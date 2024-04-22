def self.publish_software(software, screen)
    retVal      = []
    idxPosition = nil
    begin
       account 
       create_lifeshield_instance

       # -----------------------------------------
       # Logout and Login to Account Manager Login
       @lifeshield.logout unless @lifeshield.isLoginPageDisplayed
       retVal << @lifeshield.login('integration', 'Incorrect2!', 'system')
       currentPage = @lifeshield.whereAmI
       if (retVal.last.eql? true)
          retVal << eval("@lifeshield.#{currentPage}.clickSoftwareManagement()")
          currentPage = @lifeshield.whereAmI

          # -------------------------------------------------
          # Fetch all the available software versions present
          swVersions  = eval("@lifeshield.softwareManagement.getVersionColumnValues")
          swList      = swVersions.each_index.select {|version| swVersions[version] == software}
          swList.each do |idx|
             idxPosition = idx if(eval("@lifeshield.softwareManagement.getSoftwareDetails(idx+1)")['info'].include? JAR_COMPONENT_TYPE)
             break if idxPosition.present?
          end
          if idxPosition.present?
             retVal << eval("@lifeshield.#{currentPage}.clickPublish(idxPosition+1)")
             retVal << eval("@lifeshield.#{currentPage}.selectAccount(account)") rescue 'Account not present'
             publishTime = Time.now
             retVal << eval("@lifeshield.#{currentPage}.handleConfirmation('Publish')") if (retVal.last.eql? true)
             @logger.log_message("Software #{software} publish request", LogUtilities::INFO, false) if retVal.last
             retVal << Int.wait_for_sw_dl_activation('software', publishTime) if retVal.last
             @swVersion = software
             @logger.log_message('Software is published successfully', LogUtilities::INFO, false) if retVal.all?
          else
             retVal << false
             @logger.log_message("Software is not availble in #{currentPage} to publish", LogUtilities::INFO, false)
          end
       else
          @logger.log_message("Unable to login to account Manager login", LogUtilities::INFO, false)
       end
       Int.lifeshield_screen_capture("SW Publish issue") if (retVal.last.eql? false)
    rescue
       retVal << false
       Int.lifeshield_screen_capture("SW Publish issue") if (retVal.last.eql? false)
       @logger.log_message("Something went wrong in the method : #{__method__}", LogUtilities::ERROR, false)
       @logger.log_message("Exception caught: #{$!.inspect}\nError in method #{__method__}", LogUtilities::ERROR)
       @logger.log_message("Exception backtrace:\n #{$!.backtrace.join("\n")}", LogUtilities::DEBUG, false)
    ensure
       Int.handle_alarm unless (%w[PowerOff BiomedScreen].include? screen)
       form_logger_message("#{__method__} returns: | #{retVal.present? && retVal.all?} |")
       @lifeshield.logout
       return retVal.present? && retVal.all?
    end
 end
