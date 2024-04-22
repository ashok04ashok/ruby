def self.edit_interoperability_profile(action, profileDetails)
    retVal = []
    begin
       @logger.log_message("Login to Customer Account login", LogUtilities::INFO, false)
       create_lifeshield_instance
       @lifeshield.login
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickAccountConfiguration")
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.selectInteroperabilityConfiguration")
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickViewDetails(CONFIGURATION_NAME)")
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickCreateNewConfigurationVersion")
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.handleConfirmation('Yes')")
       INTEGRATION_PROFILE.each do |profile|
          case action
          when 'Add'
             profileDetails['profileType'] = profile
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickAddProfile(profile)")
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.enterProfileDetails(profileDetails)")
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickSaveProfile(profile)")
          when 'Edit'
             profileDetails['profileType'] = profile
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickEditProfile(profile)")
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.enterProfileDetails(profileDetails)")
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickSaveProfile(profile)")
          when 'Delete'
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickDeleteProfile(profile)")
             retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.handleConfirmation('Yes')")
          else
             retVal << false 
             @logger.log_message("Incorrect Action keyword - #{action} given to method #{__method__}", LogUtilities::INFO, false)
          end
       end
    rescue
       retVal << false
       @logger.log_message("Something went wrong in the method : #{__method__}", LogUtilities::ERROR, false)
       @logger.log_message("Exception caught: #{$!.inspect}\nError in method #{__method__}", LogUtilities::ERROR)
       @logger.log_message("Exception backtrace:\n #{$!.backtrace.join("\n")}", LogUtilities::DEBUG, false)
    ensure
       eval("@lifeshield.#{@lifeshield.whereAmI}.clickApproveVersion")
       @lifeshield.close
       form_logger_message("#{__method__} returns: | #{retVal.present? && retVal.all?} |")
       return retVal.present? && retVal.all?
    end
 end
