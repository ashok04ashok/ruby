# NAME
   #     self.verify_ai_detailed_view
   #
   # DESCRIPTION
   #     Method used to verify the parameters in detailed view against CDR active infusions page
   #
   # PARAMETERS
   #     cdrInputHash - CDR data for verifying against the application
   #
   # USAGE EXAMPLES
   #     self.verify_ai_detailed_view(cdrInputHash)
   #============================================================================================
   def self.verify_ai_detailed_view(cdrInputHash)
      result         = []
      totalResult    = []
      skipOptions    = IM_DETAILED_PARAMETER_SKIP.deep_dup
      programHash    = {}
      patientHash    = {}
      deviceHash     = {}
      volumeTime     = {}
      limitHash      = {}
      deviceDupHash  = {}
      standbyTime    = {}
      periodicData   = nil
      delayTime      = nil
      periodicUpdate = nil
      activeAlarm    = nil
      timeData       = nil
      locationData   = nil
      currentPage    = @lifeshield.whereAmI
      lineData       = cdrInputHash['line']
      lineMappings   = @lineMappings.invert
      ##delaySet       = Int.instance_variable_get(:@delaySet)
      ##cancelDelay    = Int.instance_variable_get(:@cancelDelay)
      ##skipLinestatus = Int.instance_variable_get(:@skipLinestatus)
      begin
         form_logger_message("Step-#{cdrInputHash['stepNo']} : Active Infusions Detailed View Details for #{lineData}")
         @postInfusion[lineData]                       = false if @postInfusion[lineData].nil?
         @continousPrecisionFlag[lineData]             = false unless cdrInputHash['currStep'].eql? @prevStepExecuted[lineMappings[lineData]]
         @postInfusion[lineData]                       = false unless cdrInputHash['currStep'].eql? @prevStepExecuted[lineMappings[lineData]]
         @doseOrRatePostInf[lineData]                  = false unless cdrInputHash['currStep'].eql? @prevStepExecuted[lineMappings[lineData]]
         @delayStartMemory[lineData]                   = nil if ((!cdrInputHash['currStep'].eql? 'step-flush') && @delayStartMemory[lineData].present? && (%w[Infusing Completed].include? cdrInputHash['infusionStatus']))
         @standbyStartMemory[lineData]                 = nil if (@standbyStartMemory[lineData].present? && (cdrInputHash['infusionStatus'].exclude? 'Standby'))
         actualTherapy                                 = cdrInputHash['lineTherapy']
         @calculationTolerance[lineMappings[lineData]] = cdrInputHash['toleranceUi'] if(cdrInputHash.key? 'toleranceUi')

         #----------------------------------------------------------
         # Get data from detailed view page based on the segregation
         detailedViewDisplay = eval("@lifeshield.#{currentPage}.isDetailViewDisplayed()")
         @logger.log_message("| Is detailedViewDisplayed for #{currentPage} #{lineMappings[lineData]} => #{detailedViewDisplay}|", LogUtilities::INFO, false)
         programDetails = eval("@lifeshield.#{currentPage}.getProgramDetails()")
         Int.lifeshield_screen_capture('Active Infusion Detailed View: Program Details')
         deviceDetails  = eval("@lifeshield.#{currentPage}.getDeviceDetails()")
         patientDetails = eval("@lifeshield.#{currentPage}.getInteroperabilityDetails()")
         Int.lifeshield_screen_capture('Active Infusion Detailed View: Interoperability Details')
         cdrInputHash.each { |inputKey, inputValue| limitHash[LIMIT_DETAILS[inputKey]] = inputValue if (LIMIT_DETAILS.keys.include? inputKey) }

         #--------------------
         # Verify Alarm Fields
         if @alarmSkip[lineMappings[lineData]].present? && (@alarmSkip[lineMappings[lineData]].eql? true)
            skipOptions    << 'Alarm Status' 
            @skipParameter << 'alarmStatus'
         else
            totalResult << alarm_verification(cdrInputHash, currentPage, lineMappings[lineData]) if (ALARM_SUPPORT.eql? true)

            #---------------------------------
            # Verify Alarm Status - Workaround
            activeAlarm = eval("@lifeshield.#{currentPage}.getColumnValues('Alarm State', 'Alarms')")
            Int.lifeshield_screen_capture('Active Infusion Detailed View: Alarm Table') if (activeAlarm.length > 2)
            @checkActiveness[lineData] = nil unless @checkActiveness[lineData].present?
            @checkActiveness[lineData] = ((activeAlarm.include? 'Active') || (activeAlarm.include? 'Silenced')) ? activeAlarm.length : 0
            @uiHash[lineMappings[lineData]]                 = {} unless @uiHash[lineMappings[lineData]].present?
            @uiHash[lineMappings[lineData]]['alarmStatus']  = {} unless @uiHash[lineMappings[lineData]]['alarmStatus'].present?
            @uiHash[lineMappings[lineData]]['alarmStatus']  = "#{@checkActiveness[lineData]} Active"
         end

         # ------------------------------------------------------
         # Clear Infusion data during new program and replace bag
         lsData = Int.instance_variable_get(:@lsData)
         if(cdrInputHash.key? "newProgram") or (lsData["replaceBag"].present? and lsData["replaceBag"].include? lineMappings[lineData])
            @clearInfusion.call(lineMappings[lineData], lineData)
            @clearFlag.call(lineMappings[lineData], lineData)
         end
         @prevStepExecuted[lineMappings[lineData]] = cdrInputHash['currStep'] unless @prevStepExecuted[lineMappings[lineData]].present?

         #-----------------------------------------------------
         # Steps not having clear condition and power off cases
         if (cdrInputHash['currentScreen'].eql? 'PowerOff') || ((cdrInputHash.key? 'clearInfusion') && (cdrInputHash['clearInfusion'].eql? true))

            #--------------------------------------------
            # Clear the therapy and volume counters clear
            @delayStartMemory[lineData]                       = nil
            @pumpValue[lineMappings[lineData]]['delayTime']   = nil unless (cdrInputHash['currentScreen'].eql? 'PowerOff' or cdrInputHash['currentScreen'].eql? 'ConfirmationScreen' or cdrInputHash['currentScreen'].eql? 'ProgramScreen')
            programHash.merge!(@uiHash[lineMappings[lineData]]['programDetails'])
            deviceHash.merge!(@uiHash[lineMappings[lineData]]['deviceDetails'])
            cdrInputHash.each { |inputKey, inputValue| patientHash[PATIENT_INFORMATION[inputKey]] = inputValue if (PATIENT_INFORMATION.keys.include? inputKey) } #ClearedLine Patient Asscociation based on otherline's AP
            programHash['Last Updated']  = programDetails['Last Updated']
            deviceHash['Power Status']   = cdrInputHash['powerStatus']
            deviceHash['Network Status'] = cdrInputHash['networkStatus']

            #-----------------------------------------------------------
            # After stop and clear - Change in volume in periodic update
            ['Volume Delivered', 'Volume Remaining'].each do |param|
               unless (programHash[param].to_f.eql? programDetails[param].to_f)
                  @logger.log_message("Value change deducted for #{param} after a line is stopped and [cleared/powered off] for #{lineData}", LogUtilities::INFO, false)
                  programHash[param] = @precisionCheck.call(param, programHash[param], programDetails[param], STOP_AND_CLEAR_TOLERANCE)
               end
            end

            #-----------------------------------------------------------
####            # After Delay/Standby stop/Clear -Time Remaining Calculation
####            if (delaySet[lineMappings[lineData]].eql? true or cancelDelay[lineMappings[lineData]].eql? true or @standbyStopped.eql? true) && !(programHash['Time Remaining'].eql? programDetails['Time Remaining'])
####               @logger.log_message("Value change deducted for Time Remaining after a line is delay/standby stopped/cancelled and [cleared/powered off] for #{lineData}", LogUtilities::INFO, false)
####               remainingTime      = calculate_time_remaining(programHash['Volume Remaining'], cdrInputHash['deliveryRateRaw'].to_f)
####               timeRemainingCheck = @toleranceCheck.call('Time Remaining', convert_pump_format_to_seconds(remainingTime), convert_pump_format_to_seconds(programDetails['Time Remaining']), TIME_REMAINING_TOLERANCE)
####               programHash['Time Remaining'] = (timeRemainingCheck.eql? true) ? programDetails['Time Remaining'] : programHash['Time Remaining']
####            end
####            @clearInfusion.call(lineMappings[lineData], lineData) if(cdrInputHash["clearInfusion"].eql? true)
####         elsif (%w[ConfirmationScreen ProgramScreen].include? cdrInputHash['currentScreen'])
####            programHash.merge!(@uiHash[lineMappings[lineData]]['programDetails'])
####            deviceHash.merge!(@uiHash[lineMappings[lineData]]['deviceDetails'])
####            patientHash.merge!(@uiHash[lineMappings[lineData]]['patientDetails'])
####            programHash['Last Updated']  = programDetails['Last Updated']
####         else
####
####            #-------------------------
####            # Detailed View Parameters
####            cdrInputHash.each do |inputKey, inputValue|
####               programHash[INFUSION_DETAILS[inputKey]]    = inputValue if (INFUSION_DETAILS.keys.include? inputKey)
####               patientHash[PATIENT_INFORMATION[inputKey]] = inputValue if (PATIENT_INFORMATION.keys.include? inputKey)
####               deviceHash[PUMP_DETAILS[inputKey]]         = inputValue if (PUMP_DETAILS.keys.include? inputKey)
####               limitHash[LIMIT_DETAILS[inputKey]]         = inputValue if (LIMIT_DETAILS.keys.include? inputKey)
####            end
####
####            #-----------------------------------------------------
####            # Resetting the bolus and flush values after titration
####            if (cdrInputHash.key? 'titration')
####               @continousPrecisionFlag[lineData]              = false
####               @doseOrRatePostInf[lineData]                   = false
####               @standbyStopped                                = nil
####               @bolusVolDelivered[lineMappings[lineData]]     = [] if @bolusVolDelivered[lineMappings[lineData]].present?
####               @flushVolDelivered[lineMappings[lineData]]     = [] if @flushVolDelivered[lineMappings[lineData]].present?
####               @prevAllStepDelivered[lineData]                = nil if @prevAllStepDelivered[lineData].present?
####               @bolusProgrammedVolume[lineMappings[lineData]] = nil if @bolusProgrammedVolume[lineMappings[lineData]].present?
####               @flushProgrammedVolume[lineMappings[lineData]] = nil if @flushProgrammedVolume[lineMappings[lineData]].present?
####            end
####
####            #--------------------------------
####            # Dose Rate Precision check 0.001
####            programHash['Dose Rate'] = @precisionCheck.call('Dose Rate', programHash['Dose Rate'], programDetails['Dose Rate'], DOSERATE_PRECISION_TOLERANCE) \
####               if ((programHash.key? 'Dose Rate') && !(programHash['Dose Rate'].to_f.eql? programDetails['Dose Rate'].to_f) && !(programHash['Dose Rate'].eql? NA))
####
####            #----------------------------------------------------
####            # Programmed Volume Precision normal check with 0.001
####            programHash['Programmed Volume'] = @precisionCheck.call('Programmed Volume', programHash['Programmed Volume'], programDetails['Programmed Volume'], VTBI_PRECISION_TOLERANCE) \
####               unless (programHash['Programmed Volume'].to_f.eql? programDetails['Programmed Volume'].to_f)
####
####            #------------------------------------------------------------------------------------
####            # Programmed Volume Precision check after clear bolus || titrationFlag is set to true
####            @continousPrecisionFlag[lineData] = true if (cdrInputHash.key? 'clearBolus') && (cdrInputHash['clearBolus'].eql? true)
####            programHash['Programmed Volume']  = @precisionCheck.call('Programmed Volume', programHash['Programmed Volume'], programDetails['Programmed Volume'], CLEAR_BOLUS_PV_TOLERANCE) \
####               if ((@continousPrecisionFlag[lineData].eql? true) || (@titrationFlag[lineData].eql? true))
####
####            # -------------------------------------------
####            # Programmed Duration rounding check to 1 min
####            programHash['Programmed Duration'] = convert_seconds_to_pump_format(@precisionCheck.call('Programmed Duration', convert_pump_format_to_seconds(programHash['Programmed Duration']), convert_pump_format_to_seconds(programDetails['Programmed Duration']), CLEAR_BOLUS_PD_TOLERANCE)) \
####               unless (programHash['Programmed Duration'].eql? programDetails['Programmed Duration'])
####
####            #------------------------------
####            # Dose / DoseOrRate Computation
####            ['hr', 'min', 'day', '/h'].each do |word|
####               if (programHash['Dose'].include? word)
####                  programHash['Dose Rate'] = programHash['Dose']
####                  programHash['Dose']      = NA
####                  break
####               else
####                  programHash['Dose Rate'] = NA unless programHash['Dose Rate'].present?
####               end
####            end
####
####            #---------------------------------
            # Collect Initial Volume delivered
            @uiHash[lineMappings[lineData]]                   = {} unless @uiHash[lineMappings[lineData]].present?
            @uiHash[lineMappings[lineData]]['programDetails'] = {} unless @uiHash[lineMappings[lineData]]['programDetails'].present?
            if !(cdrInputHash.key? "newProgram") && (cdrInputHash['infusionStatus'].eql? @uiHash[lineMappings[lineData]]['programDetails']['Infusion Status']) && (cdrInputHash['currStep'].eql? @prevStepExecuted[lineMappings[lineData]]) && !(cdrInputHash.key? 'titration') && !(lsData["replaceBag"].present? and lsData["replaceBag"].include? lineMappings[lineData])
               initialVolume = @uiHash[lineMappings[lineData]]['programDetails']['Volume Delivered']
               periodicData  = true
            else
               initialVolume = calculate_volume_infused(@pumpValue[lineMappings[lineData]]['volumeDelivered'], cdrInputHash, actualTherapy)
            end

            # ---------------------------
            # Fetching detail view Volume
            detailedVolume     = programDetails[INFUSION_DETAILS['volumeDelivered']]
            detailedViewVolume = detailedVolume

            #------------------------------------------------
            # Getting latest volume and rate from the infuser
            deliveryHash    = get_volume_and_rate(lineData, cdrInputHash) unless (%w[ConfirmationScreen ProgramScreen].include? cdrInputHash['currentScreen'])
            currentRate     = cdrInputHash['deliveryRateRaw']
            @logger.log_message("calculationTolerance : #{@calculationTolerance}", LogUtilities::INFO, false)
            toleratedVolume = calculate_vtbi(currentRate, @calculationTolerance[lineMappings[lineData]])

            # ----------------------
            # End Volume calculation
            endVolume = calculate_volume_infused(deliveryHash[lineMappings[lineData]]['volumeDelivered'].to_f, cdrInputHash, actualTherapy, false) + toleratedVolume + END_VOLUME_TOLERANCE

            # -------------------------------
            # Logging the volume informations
            @logger.log_message("Wrapper Clear Volume Counter : #{Int.instance_variable_get(:@volumeCounters)}", LogUtilities::INFO, false)
            form_logger_message("Initial Volume : #{@pumpValue[lineMappings[lineData]]['volumeDelivered']}, Latest Volume : #{deliveryHash[lineMappings[lineData]]['volumeDelivered'].to_f} , toleranceApplied : #{toleratedVolume}")

            #-------------
            # Collect time
            @initialTime[lineMappings[lineData]] = {} unless @initialTime[lineMappings[lineData]].present?
            startTime                            = @pumpValue[lineMappings[lineData]]['currentTimeData'].present? ? @pumpValue[lineMappings[lineData]]['currentTimeData'] : @initialTime[lineMappings[lineData]]
            @initialTime[lineMappings[lineData]] = startTime

            #----------------------------------------------------
            # Truncate the precision values when greater than 100
            VOLUMES.each_with_index { |v1, index| eval("#{VOLUMES[index]} = (#{v1}.to_f >= 100) ? #{v1}.to_f.truncate : #{v1}.to_f.truncate(2)") }

            #---------------------------------------------------
            # Compare the volume based on Periodic and Aperiodic
            if (periodicData.eql? true)
               form_logger_message('==> PROCESSING PERIODIC INFORMATION <==')
               operator = ((cdrInputHash.key? 'periodicInfo') && (cdrInputHash['periodicInfo'].eql? true) && (cdrInputHash['infusionStatus'].eql? 'Infusing')) ? '<' : '<='
               expectedVolume = (eval("initialVolume.to_f.truncate(1) #{operator} detailedViewVolume.to_f") && (detailedViewVolume.to_f <= endVolume.to_f)) ? detailedVolume.to_f : endVolume.to_f
               programHash['Volume Delivered'] = "#{convert_number(expectedVolume)} mL"
               condition = initialVolume
            else
               initialCheck    = ((initialVolume.to_f - toleratedVolume.to_f) <= detailedViewVolume.to_f)
               differenceCheck = ((initialVolume.to_f - toleratedVolume.to_f - detailedVolume.to_f) <= 1)
               expectedVolume  = ((initialCheck || differenceCheck) && (detailedViewVolume.to_f <= endVolume.to_f)) ? detailedVolume.to_f : endVolume.to_f
               programHash['Volume Delivered'] = "#{convert_number(expectedVolume)} mL"
               condition = (initialVolume.to_f - toleratedVolume.to_f)
            end
            @logger.log_message("|#{'-' * 130}|", LogUtilities::INFO, false)
            @logger.log_message("| Initial Volume #{' ' * (40 - 'Initial Volume'.to_s.length)}| Detailed View Volume #{' ' * (40 - 'Detailed View Volume'.to_s.length)}| Latest Volume #{' ' * (42 - 'Latest Volume'.to_s.length)}|", LogUtilities::INFO, false)
            @logger.log_message("| #{condition} #{' ' * (39 - condition.to_s.length)} #{operator} #{detailedViewVolume}  #{' ' * (40 - detailedViewVolume.to_s.length)} #{operator} #{endVolume}  #{' ' * (42 - endVolume.to_s.length)}|", LogUtilities::INFO, false)
            @logger.log_message("|#{'-' * 130}|", LogUtilities::INFO, false)

            #------------------------------------
            # Calculate Volume and Time remaining
            if (cdrInputHash['infusionStatus'].include? 'Completed' and !cdrInputHash['callbackStopped'].eql? true)
               @logger.log_message("ConfiguredPostInfusion: #{cdrInputHash['postInfusion']} , Value : #{cdrInputHash['postInfusionVal']}", LogUtilities::INFO, false)
               @postInfusion[lineData] = true if ((['VTBI COMPLETE - KVO', 'VTBI COMPLETE - RATE', 'COMPLETED', 'STOPPED'].include? cdrInputHash['lineStatus']) || ((cdrInputHash['postInfusion'].include? 'stop') && (cdrInputHash['infusionStatus'].eql? 'Completed')))
               @doseOrRatePostInf[lineData]    = true if (['VTBI COMPLETE - KVO', 'VTBI COMPLETE - RATE'].include? cdrInputHash['lineStatus'])
               programHash['Delivery Rate']    = "#{cdrInputHash['postInfusionVal']} mL/hr" if ((!cdrInputHash['postInfusion'].include? 'rate') && ((cdrInputHash['infusionStatus'].eql? 'Completed (Post Infusion)') || (@uiHash[lineMappings[lineData]]['programDetails']['Delivery Rate'].eql? "#{cdrInputHash['postInfusionVal']} mL/hr")))
               programHash['Volume Remaining'] = '0 mL'
               programHash['Time Remaining']   = '0 hr 0 min'
            else
               volumeTime    = calculate_volume_and_time_remaining(programHash, cdrInputHash, lineData)
               timeRemaining = volumeTime['Time Remaining']

               # ------------------------------------------------
               # Time Remaining calculation for Delay and Standby
               if (%w[delayStart standbyStart].any?{|key| cdrInputHash.keys.include? key})
                  therapyType    = cdrInputHash["delayStart"].present? ? 'delay' : 'standby'
                  programmedTime = eval("convert_seconds_to_pump_format(convert_pump_format_to_seconds(cdrInputHash['#{therapyType}Start']))")
                  eval("@#{therapyType}StartMemory[lineData] = programmedTime ")
                  volumeTime['Time Remaining'] = (%w[Delayed Standby].include? cdrInputHash['infusionStatus']) ? programmedTime : timeRemaining
               # Delay and Standby - Code change => @HCA-2266
               elsif (%w[Delayed Standby].include? cdrInputHash['infusionStatus'])
                  therapyType = (cdrInputHash["infusionStatus"].eql? 'Delayed')? 'delay' : 'standby'
                  if eval("@pumpValue[lineMappings[lineData]]['#{therapyType}Time'].present?")
                     previousDuration = eval("convert_pump_format_to_seconds(@#{therapyType}StartMemory[lineData])")
                     currentDuration  = eval("convert_pump_format_to_seconds(@pumpValue[lineMappings[lineData]]['#{therapyType}Time'])")
                     endDuration      = eval("convert_pump_format_to_seconds(deliveryHash[lineMappings[lineData]]['#{therapyType}Time'])")
                     actualValue      = convert_pump_format_to_seconds(programDetails['Time Remaining'])
                     periodicCheck    = ((previousDuration - currentDuration) > 300) ? true : false
                     operator         = (periodicCheck.eql? false) ? '>=' : '>'
                     rangeCheck       = (eval("previousDuration #{operator} actualValue") && (actualValue >= endDuration) && (currentDuration < previousDuration)) ? true : false
                     eval("@#{therapyType}StartMemory[lineData] = volumeTime['Time Remaining'] = ((rangeCheck.eql? true)? programDetails['Time Remaining'] : convert_seconds_to_pump_format(#{currentDuration}))")
                     @logger.log_message("|#{'-' * 130}|", LogUtilities::INFO, false)
                     @logger.log_message("| (previousDuration #{operator} actualValue) and (actualValue >= endDuration) and (currentDuration < previousDuration)| ", LogUtilities::INFO, false)
                     @logger.log_message("| ((#{previousDuration} #{operator} #{actualValue}) and (#{actualValue} >= #{endDuration}) and (#{currentDuration} < #{previousDuration}))", LogUtilities::INFO, false)
                     @logger.log_message("|#{'-' * 130}|", LogUtilities::INFO, false)
                  else
                     volumeTime['Time Remaining'] = timeRemaining
                  end
               else
                  volumeTime['Time Remaining'] = timeRemaining
               end

               #-----------------------------------------------
####               # Adding Tolerence of 1 min for Volume Remaining
####               volumeTolerence      = calculate_vtbi(cdrInputHash['deliveryRateRaw'], SIXTY_SEC_TOLERANCE)
####               volumeToleranceCheck = @toleranceCheck.call('Volume Remaining', "#{volumeTime['Volume Remaining']} mL", programDetails[INFUSION_DETAILS['volumeRemaining']], volumeTolerence)
####               if (volumeToleranceCheck.eql? true)
####                  programHash['Volume Remaining'] = programDetails[INFUSION_DETAILS['volumeRemaining']]
####               else
####                  #----------------------------------------------
####                  # Adding Tolerence of 1 mL for Volume Remaining
####                  form_logger_message('** Second Tolerance check for Volume Remaining **')
####                  volumeToleranceCheck = @toleranceCheck.call('Volume Remaining', "#{volumeTime['Volume Remaining']} mL", programDetails[INFUSION_DETAILS['volumeRemaining']], (volumeTolerence+VOLUME_REMAINING_TOLERANCE))
####                  programHash['Volume Remaining'] = (volumeToleranceCheck.eql? true) ? programDetails[INFUSION_DETAILS['volumeRemaining']] : "#{volumeTime['Volume Remaining']} mL"
####               end
####               if (%w[Delayed Standby].include? cdrInputHash['infusionStatus'])
####                  timeToleranceCheck = @toleranceCheck.call('Time Remaining', convert_pump_format_to_seconds(volumeTime['Time Remaining']),convert_pump_format_to_seconds(programDetails[INFUSION_DETAILS['timeRemaining']]), TIME_REMAINING_TOLERANCE)
####                  programHash['Time Remaining'] = (timeToleranceCheck.eql? true) ? programDetails[INFUSION_DETAILS['timeRemaining']] : volumeTime['Time Remaining']
####               else
####
####                  #---------------------------------------------------------------------------------------------
####                  # Adding Tolerence of 60 seconds for Time Remaining with respect to Finalized Volume Remaining
####                  initialTime        = calculate_time_remaining(programHash['Volume Remaining'], cdrInputHash['deliveryRateRaw'].to_f)
####                  timeToleranceCheck = @toleranceCheck.call('Time Remaining', convert_pump_format_to_seconds(initialTime), convert_pump_format_to_seconds(programDetails[INFUSION_DETAILS['timeRemaining']]), TIME_REMAINING_TOLERANCE)
####
####                  # ---------------------------------------------------------------------------------------------
####                  # Delay/Standby Stop - Checking for remaining programmed time / Remaining delay time while stop
####                  if (timeToleranceCheck.eql? false) && (cdrInputHash['infusionStatus'].eql? "Stopped") && (delaySet[lineMappings[lineData]].eql? true or cancelDelay[lineMappings[lineData]].eql? true or @uiHash[lineMappings[lineData]]['programDetails']['Infusion Status'].eql? 'Standby')
####                     if(@uiHash[lineMappings[lineData]]['programDetails']['Infusion Status'].eql? 'Standby')
####                        stoppedTime     = Int.instance_variable_get(:@remainingStandby)
####                        therapy         = 'Standby'
####                        @standbyStopped = true
####                     else
####                        stoppedTime = Int.instance_variable_get(:@remainingDelay)
####                        therapy     = 'Delayed'
####                     end
####                     form_logger_message("#{therapy} - Stop/Cancel - Check => #{stoppedTime}")
####                     timeToleranceCheck = @toleranceCheck.call('Time Remaining', convert_pump_format_to_seconds(stoppedTime[lineMappings[lineData]]), convert_pump_format_to_seconds(programDetails[INFUSION_DETAILS['timeRemaining']]), TIME_REMAINING_TOLERANCE) if(stoppedTime.present?)
####                  end
####                  programHash['Time Remaining'] = (timeToleranceCheck.eql? true) ? programDetails[INFUSION_DETAILS['timeRemaining']] : volumeTime['Time Remaining']
####               end
####            end
            if ((periodicData.eql? true) && (LAST_UPDATED.eql? true))
               #------------------
               # Skip Last Updated
               skipOptions    << 'Last Updated' if (LAST_UPDATED.eql? true) && (periodicData.eql? true)
               @skipParameter << 'lastUpdated' if (LAST_UPDATED.eql? true) && (periodicData.eql? true)
            else
               timeData          = @uiHash[lineMappings[lineData]]['programDetails']['Last Updated'].present? ? @uiHash[lineMappings[lineData]]['programDetails']['Last Updated'] : '0:0'
               periodicUpdate    = (@uiHash[lineMappings[lineData]]['programDetails']['Last Updated'].to_s.include? 'Last') ? @uiHash[lineMappings[lineData]]['programDetails']['Last Updated'] : Time.parse(timeData).strftime('%s').to_i
               initialUpdateTime = (periodicData.eql? true) ? periodicUpdate : (Time.parse(@initialTime[lineMappings[lineData]].to_s).strftime('%s').to_i - (@pumpValue[lineMappings[lineData]]['timeDiff'].to_i + 10))
               detailedViewTime  = (programDetails['Last Updated'].to_s.include? 'Last') ? programDetails['Last Updated'] : Time.parse((programDetails['Last Updated'])).strftime('%s').to_i
               endUpdateTime     = Time.parse(deliveryHash[lineMappings[lineData]]['currentTimeData'].to_s).strftime('%s').to_i
               @logger.log_message("|Time timeDiff: #{@pumpValue[lineMappings[lineData]]['timeDiff']}|", LogUtilities::INFO, false)
               programHash['Last Updated'] = ((initialUpdateTime.to_f <= detailedViewTime.to_f) && (detailedViewTime.to_f <= endUpdateTime.to_f)) ? programDetails['Last Updated'].to_s : Time.parse(deliveryHash[lineMappings[lineData]]['currentTimeData'].to_s).strftime('%Y-%m-%d %H:%M:%S')
               @logger.log_message("|#{'-' * 130}|", LogUtilities::INFO, false)
               @logger.log_message("| Initial Time #{' ' * (40 - 'Initial Time'.to_s.length)}| Detailed Last Updated Time #{' ' * (40 - 'Detailed Last Updated Time'.to_s.length)}| Latest Updated Time #{' ' * (42 - 'Latest Updated Time'.to_s.length)}|", LogUtilities::INFO, false)
               @logger.log_message("| #{@pumpValue[lineMappings[lineData]]['currentTimeData']} #{' ' * (39 - @pumpValue[lineMappings[lineData]]['currentTimeData'].to_s.length)} <= #{programDetails['Last Updated']}  #{' ' * (40 - programDetails['Last Updated'].to_s.length)} <= #{deliveryHash[lineMappings[lineData]]['currentTimeData']}  #{' ' * (42 - deliveryHash[lineMappings[lineData]]['currentTimeData'].to_s.length)}|", LogUtilities::INFO, false)
               @logger.log_message("| #{initialUpdateTime} #{' ' * (39 - initialUpdateTime.to_s.length)} <= #{detailedViewTime}  #{' ' * (40 - detailedViewTime.to_s.length)} <= #{endUpdateTime}  #{' ' * (42 - endUpdateTime.to_s.length)}|", LogUtilities::INFO, false)
               @logger.log_message("|#{'-' * 130}|", LogUtilities::INFO, false)
            end
         end
         @logger.log_message("postInfusionFlag => #{@postInfusion[lineData]}", LogUtilities::INFO, false)
         @logger.log_message("doseOrRateFlag => #{@doseOrRatePostInf[lineData]}, standAlonebolus => #{@standAloneBolus[lineData]}", LogUtilities::INFO, false)
         @logger.log_message("prevVolDelivered => #{@prevVolDelivered[lineMappings[lineData]]}", LogUtilities::INFO, false) if @prevVolDelivered[lineMappings[lineData]].present?
         @logger.log_message("stepVolDelivered => #{@stepVolDelivered[lineMappings[lineData]]}", LogUtilities::INFO, false) if @stepVolDelivered[lineMappings[lineData]].present?
         @logger.log_message("standAlonebolus => #{@standAloneBolusVolDel[lineMappings[lineData]]}", LogUtilities::INFO, false) if @standAloneBolusVolDel[lineMappings[lineData]].present?
         @logger.log_message("bolusVolDelivered => #{@bolusVolDelivered[lineMappings[lineData]]}", LogUtilities::INFO, false) if @bolusVolDelivered[lineMappings[lineData]].present?
         @logger.log_message("BolusCumulativeVolDelivered => #{@pumpCumBolusVolDelivered[lineMappings[lineData]]}", LogUtilities::INFO, false) if @pumpCumBolusVolDelivered[lineMappings[lineData]].present?
         @logger.log_message("flushVolDelivered => #{@flushVolDelivered[lineMappings[lineData]]}", LogUtilities::INFO, false) if @flushVolDelivered[lineMappings[lineData]].present?
         @logger.log_message("FlushCumulativeVolDelivered => #{@pumpCumFlushVolDelivered[lineMappings[lineData]]}", LogUtilities::INFO, false) if @pumpCumFlushVolDelivered[lineMappings[lineData]].present?
         @logger.log_message("beforePostInfVolDelivered => #{@beforePostInfVolDelivered[lineMappings[lineData]]}", LogUtilities::INFO, false) if @beforePostInfVolDelivered[lineMappings[lineData]].present?

         #-----------------------------------------------------------------
         # Skip Clear Bolus / Clear Load / Callback Stopped - Entire fields
         if ((skipLinestatus.eql? true) || ((CLEAR_BOLUS.eql? true) && cdrInputHash['clearBolus']) || ((CLEAR_LOAD.eql? true) && cdrInputHash['clearLoad']) || ((CALLBACK_STOPPED.eql? true) && cdrInputHash['callbackStopped']) || (%w[ConfirmationScreen ProgramScreen].include? cdrInputHash['currentScreen']))

            #---------------------------------------------------------
            # Skipping parameters leads to false in the method calling
            @uiHash[lineMappings[lineData]]['programDetails'] = programHash
            @uiHash[lineMappings[lineData]]['deviceDetails']  = deviceHash
            @uiHash[lineMappings[lineData]]['limitDetails']   = limitHash
            @uiHash[lineMappings[lineData]]['patientDetails'] = patientHash
            totalResult << true
         else
         	
            #-------------------------------
            # Skip fields in program Details
            programHash.each_key { |field| programHash.delete(field) if (skipOptions.include? field) } if skipOptions.present?

            #-----------------
            # Infusion Details
            form_logger_message('Infusion Details')
            temp = nil
            programHash.each do |key, value|
               values = nil
               if (key.eql? 'Medication')
                  values           = { 'medication' => value[0].to_s, 'highRisk' => value[1] }
                  temp             = programHash[key]
                  programHash[key] = values
               else
                  values = value
               end
               result << (programDetails[key].eql? values)
            end
            totalResult << result.all?
            form_logger_design(programHash, programDetails, result)
            programHash['Medication']                         = temp
            @uiHash[lineMappings[lineData]]['programDetails'] = programHash
            result.clear

            #------------------------------
            # Skip fields in Device Details
            deviceHash.each_key { |field| deviceHash.delete(field) if (skipOptions.include? field) } if skipOptions.present?

            #-------------
            # Pump Details
            form_logger_message('Pump Details')
            deviceDupHash = Marshal.load(Marshal.dump(deviceHash))
            deviceHash.each do |key, value|
               #-------------------------------------------------------
               # Delete Unwanted hash key from Network and Power status
               %w[tooltip level].each { |val| deviceDetails[key].delete(val) } if (['Power Status', 'Network Status'].include? key)

               #-----------------
               # Location mapping
               if (key.eql? 'Location')

                  #-----------------------------------------
                  # Previous and Current location comparison
                  if @imLocation.present?
                     locationData = (@imLocation.eql? deviceDetails[key]) ? 'Same' : 'Different'
                     @logger.log_message("Infuser Network Location is #{locationData} | Previous-step => #{@imLocation}| current-step => #{deviceDetails[key]}|", LogUtilities::INFO, false)
                  end
                  result << (value.include? deviceDetails[key])
                  @imLocation = deviceDetails[key]
                  deviceDupHash[key] = result.last ? deviceDetails[key] : value.last
               else
                  result << (deviceDetails[key].eql? value)
               end
            end
            totalResult << result.all?
            form_logger_design(deviceDupHash, deviceDetails, result)
            @uiHash[lineMappings[lineData]]['deviceDetails'] = deviceHash
            result.clear

            #--------------
            # Limit Details
            @tabularLimit['limitIconData'] = []
            if (LIMIT_SUPPORT.eql? true)
               form_logger_message('Limit Details')
               if ((BOLUS_FLUSH_LIMIT_SKIP.eql? true) && (cdrInputHash['skipLimit'].eql? true))
                  @logger.log_message('Limit Alert Has been skipped', LogUtilities::INFO, false)
               else
                  result      << limit_verification(limitHash, lineData)
                  totalResult << result.last
                  @uiHash[lineMappings[lineData]]['limitDetails'] = limitHash
                  @tabularLimit['limitIconData']                  = [false] unless limitHash.present?
                  result.clear
               end
            else
               @tabularLimit['limitIconData'] = [false]
            end

            #-------------------------------
            # Skip fields in patient Details
            returnValue = @programSourceUi.call(cdrInputHash['programSource'])
            patientHash['Program Source Tooltip']    = returnValue['tooltip']
            patientHash['Program Source']            = returnValue['source']
            actualProgramSourceTooltip               = @lifeshield.activeInfusions.getDetailViewTooltip('Program Source')
            patientDetails['Program Source Tooltip'] = (actualProgramSourceTooltip.eql? 'No tooltip present.')? 'No icon present' : actualProgramSourceTooltip
            patientHash.each_key { |field| patientHash.delete(field) if (skipOptions.include? field) } if skipOptions.present?

            #----------------------
            # Auto Program  Details
            if (INTEROPERABILITY_SUPPORT.eql? true)
               form_logger_message('Auto Program Details')
               patientHash.each do |key, value|
                  result << (patientDetails[key].eql? value)
               end
               totalResult << result.all?
               form_logger_design(patientHash, patientDetails, result)
               result.clear
            end
            @uiHash[lineMappings[lineData]]['patientDetails'] = patientHash
         end
      rescue
         totalResult << false
         @logger.log_message("Something went wrong in method: #{__method__} in line #{__LINE__}", LogUtilities::ERROR, false)
         @logger.log_message("Exception caught: #{$!.inspect}\nError in method #{__method__}", LogUtilities::ERROR)
         @logger.log_message("Exception backtrace:\n #{$!.backtrace.join("\n")}", LogUtilities::DEBUG, false)
      ensure
         eval("@lifeshield.#{currentPage}.clickClose()")
         return totalResult.present? && totalResult.all?
      end
   end

   #===========================================================================================
   # NAME
   #     self.verify_ai_tabular_view
   #
   # DESCRIPTION
   #     Method used to verify the parameters in tabular view against CDR active infusions page
   #
   # PARAMETERS
   #     cdrInputHash - CDR Active infusion data for verifying against the application
   #
   # USAGE EXAMPLES
   #     self.verify_ai_tabular_view(cdrInputHash)
   #===========================================================================================
   def self.verify_ai_tabular_view(cdrInputHash)
      actualValue      = {}
      aiTableViewInput = {}
      aiMapping        = {}
      result           = []
      lineMappings     = @lineMappings.invert
      skipOptions      = []
      actualLimitIcon  = []
      aiInputHash      = Marshal.load(Marshal.dump(cdrInputHash))
      indexVal         = 1
      loopVal          = 12
      skipLinestatus   = Int.instance_variable_get(:@skipLinestatus)
      begin
         skipOptions       = IM_TABULAR_PARAMETER_SKIP.deep_dup + @skipParameter
         lineData          = cdrInputHash['line']
         currentPage       = @lifeshield.whereAmI
         channelArray      = eval("@lifeshield.#{currentPage}.getColumnValues('Line', 'Active Infusions')")
         channelIndex      = channelArray.find_index(cdrInputHash['line']) + 1 if cdrInputHash['line'].present? && channelArray.present?
         actualTableValue  = eval("@lifeshield.#{currentPage}.getTableRow(channelIndex, 'Active Infusions')")
         actualHeaderValue = eval("@lifeshield.#{currentPage}.getHeaderLabels()")
         remainingData     = actualHeaderValue.length
         while (loopVal <= actualHeaderValue.length || !(remainingData.eql? 0))
            remainingData = (loopVal <= actualHeaderValue.length) ? (actualHeaderValue.length - loopVal) : 0
            locatorVal    = (remainingData.eql? 0) ? actualHeaderValue.length : loopVal
            tableLocator  = "{\"xpath\": \"//div[contains(@class,'icu-mat-table')]//th[#{locatorVal}]\"}"
            eval("@lifeshield.#{currentPage}.scrollIntoView("+tableLocator+")")
            Int.lifeshield_screen_capture("Active Infusion Tabular View - #{indexVal}: #{lineData}")
            indexVal += 1
            loopVal  += 12
         end

         #---------------------------------------------------------
         # Resetting the scroll view back to point the first header
         tableLocator = "{\"xpath\": \"//div[contains(@class,'icu-mat-table')]//th[1]\"}"
         eval("@lifeshield.#{currentPage}.scrollIntoView("+tableLocator+")")

         #------------------------------------
         # Assigning the actual values in Hash
         actualHeaderValue.each_with_index { |header, index| actualValue[header] = actualTableValue[index] }
         aiMapping.merge!(AI_TABULAR_MAPPING).merge!(PATIENT_INFORMATION)
         aiInputHash.each { |inputKey, inputValue| aiTableViewInput[inputKey] = inputValue if (aiMapping.include? inputKey) }
         form_logger_message("Step-#{cdrInputHash['stepNo']} : Active Infusions Tabular View Details for #{lineData}")

         #--------------------------------------------
         # Map High Alert medication from UI to Actual
         actualValue['highAlertMedication'] = eval("@lifeshield.#{currentPage}.isHighAlertMedication(aiInputHash['serialNumber'], lineData)")

         #-------------------------------------
         # Program Source Mapping for AP/Manual
         returnValue = @programSourceUi.call(aiInputHash['programSource'])
         aiTableViewInput['programSource'] = returnValue['source']
         if(PROGRAM_SOURCE_TOOLTIP_CHECK.eql? true)
            aiTableViewInput['programSourceTooltip'] = returnValue['tooltip']
            programSource = eval("@lifeshield.#{currentPage}.getProgramSourceInfo(aiInputHash['serialNumber'], lineData)")
            actualValue['Program Source Tooltip'] = programSource['tooltip'].present? ? programSource['tooltip'] : 'No icon present'
         end

         #-----------------------------------------
         # Map Limit Icon Verification UI to Actual
         iconData = eval("@lifeshield.#{currentPage}.getSoftLimitOverridesColumnValues")[channelArray.find_index(cdrInputHash['line'])]
         actualLimitIcon << ((iconData.eql? "") ? false : iconData)
         actualValue['limitIconData'] = actualLimitIcon
         actualValue['limitIconData'].flatten!
         actualValue['limitIconData'] = actualValue['limitIconData'].sort!
         @tabularLimit['limitIconData'].uniq!
         aiTableViewInput['limitIconData'] = @tabularLimit['limitIconData'].sort!

         #-------------------------------------
         # Medication verification - High Alert
         aiTableViewInput['medication']          = aiInputHash['medication'][0]
         aiTableViewInput['highAlertMedication'] = aiInputHash['medication'][1]

         #-----------------------------------------------
         # Get the volume and time remaininng from memory
         aiTableViewInput['volumeRemaining'] = @uiHash[lineMappings[lineData]]['programDetails']['Volume Remaining'] if @uiHash[lineMappings[lineData]]['programDetails']['Volume Remaining'].present?
         aiTableViewInput['timeRemaining']   = @uiHash[lineMappings[lineData]]['programDetails']['Time Remaining'] if @uiHash[lineMappings[lineData]]['programDetails']['Time Remaining'].present?
         aiTableViewInput['programMode']     = @uiHash[lineMappings[lineData]]['programDetails']['Program Mode'] if @uiHash[lineMappings[lineData]]['programDetails']['Program Mode'].present?
         aiTableViewInput['lastUpdated']     = (actualValue['Last Updated'].downcase.include? 'last') ? actualValue['Last Updated'] : @uiHash[lineMappings[lineData]]['programDetails']['Last Updated']

         #----------------------
         # Dose/Rate Computation
         if @uiHash[lineMappings[lineData]]['programDetails']['Program Mode'].present?
            programMode    = @uiHash[lineMappings[lineData]]['programDetails']['Program Mode']
            dosingUnitType = (@uiHash[lineMappings[lineData]]['programDetails']['Dose'].eql? 'N/A') ? 'timeBased' : 'nonTimeBased'
            if (@uiHash[lineMappings[lineData]]['programDetails']['Infusion Status'].include? 'Completed') && (@doseOrRatePostInf[cdrInputHash['line']].eql? true)
               doseOrRate = @uiHash[lineMappings[lineData]]['programDetails']['Delivery Rate']
            elsif (programMode.downcase.include? 'flush')
               doseOrRate = @uiHash[lineMappings[lineData]]['programDetails']['Delivery Rate']
            elsif (dosingUnitType.eql? 'timeBased') && (@uiHash[lineMappings[lineData]]['programDetails']['Dose Rate'].eql? NA)
               doseOrRate = @uiHash[lineMappings[lineData]]['programDetails']['Delivery Rate']
            elsif (programMode.downcase.include? 'bolus') || (dosingUnitType.eql? 'nonTimeBased')
               doseOrRate = @uiHash[lineMappings[lineData]]['programDetails']['Dose']
            elsif !(programMode.downcase.include? 'bolus') && (dosingUnitType.eql? 'timeBased')
               doseOrRate = @uiHash[lineMappings[lineData]]['programDetails']['Dose Rate']
            elsif !(programMode.downcase.include? 'bolus') && (@uiHash[lineMappings[lineData]]['programDetails']['Dose Rate'].include? 'mL/hr')
               doseOrRate = @uiHash[lineMappings[lineData]]['programDetails']['Delivery Rate']
            end
            aiTableViewInput['doseOrRate'] = doseOrRate
         end

         #--------------------------
         # Alarm status verification
         aiTableViewInput['alarmStatus'] = @uiHash[lineMappings[lineData]]['alarmStatus']
         if ((skipLinestatus.eql? true) || ((CLEAR_BOLUS.eql? true) && aiInputHash['clearBolus']) || ((CLEAR_LOAD.eql? true) && aiInputHash['clearLoad']) || ((CALLBACK_STOPPED.eql? true) && aiInputHash['callbackStopped']) || (%w[ConfirmationScreen ProgramScreen].include? aiInputHash['currentScreen']))

            #---------------------------------------------------------
            # Skipping parameters leads to false in the method calling
            result << true
         else

            #-------------------------------
            # Skip fields in patient Details
            aiTableViewInput.each_key { |field| aiTableViewInput.delete(field) if (skipOptions.include? field) } if skipOptions.present?

            #---------------------------------------
            # Iterate the views and form the results
            aiTableViewInput.each { |aiTableKey, aiTableValue| result << (actualValue[aiMapping[aiTableKey]].to_s.strip.eql? aiTableValue.to_s.strip) }
            form_logger_design(aiTableViewInput, actualValue, result, aiMapping)
         end
      rescue
         result << false
         @logger.log_message("Something went wrong in method: #{__method__}", LogUtilities::ERROR, false)
         @logger.log_message("Exception caught: #{$!.inspect}\nError in method #{__method__}", LogUtilities::ERROR)
         @logger.log_message("Exception backtrace:\n #{$!.backtrace.join("\n")}", LogUtilities::DEBUG, false)
      ensure
         @skipParameter = []
         return result.present? && result.all?
      end
   end
