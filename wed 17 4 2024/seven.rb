def self.verify_dm_row_greyout()
    retVal = []
    begin
       create_lifeshield_instance
       retVal << mednet_cloud_navigation('deviceList')
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.isRowGrayedOut('#{@staticInformation['deviceName']}')")
       @logger.log_message("Is row greyed out in Device List: #{retVal.last}", LogUtilities::INFO, false)
       unless @lifeshield.isLoginPageDisplayed
          retVal << @lifeshield.logout
          @logger.log_message("Logged out from Lifeshield: #{retVal.last}", LogUtilities::INFO, false)
       end
    rescue
       @logger.log_message("Something went wrong in the method : #{__method__}", LogUtilities::ERROR, false)
       @logger.log_message("Exception caught: #{$!.inspect}\nError in method #{__method__}", LogUtilities::ERROR)
       @logger.log_message("Exception backtrace:\n #{$!.backtrace.join("\n")}", LogUtilities::DEBUG, false)
    ensure
       @lifeshield.close unless @lifeshield.nil?
       form_logger_message("#{__method__} returns: | #{retVal.present? && retVal.all?} |")
       return retVal.present? && retVal.all?
    end
 end