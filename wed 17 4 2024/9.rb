def self.set_ivehr_interoperability(flag)
    retVal = []
    text   = (flag.eql? true) ? 'Enable' : 'Disable'
    begin
       @logger.log_message("Login to Customer Account login", LogUtilities::INFO, false)
       create_lifeshield_instance
       @lifeshield.login
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickAccountConfiguration")
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.selectConnectivityManagement")
       nodeList  = eval("@lifeshield.#{@lifeshield.whereAmI}.getColumnValues('Name')")
       @logger.log_message("Connectivity Adapter Available : #{nodeList}  -- Input CA node name : #{NODE_NAME}", LogUtilities::INFO, false)
       nodeIndex = nodeList.find_index(NODE_NAME)
       @logger.log_message("Index of the node #{nodeIndex+1} && Node name #{NODE_NAME}", LogUtilities::INFO, false)
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.selectRowOption(nodeIndex+1, 'View Details')")
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickNodeSettingsEdit()")
       @logger.log_message("Edit button click in Node settings : #{retVal.last}", LogUtilities::INFO, false)
       condition = (flag.eql? false) ? '!' : ''
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.enableInteroperability(#{flag})")
       options = eval("@lifeshield.#{@lifeshield.whereAmI}.getInteroperabilityConfigurationOptions") if (flag.eql? true)
       @logger.log_message("Available Configuration Option : #{options}", LogUtilities::INFO, false)
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.selectInteroperabilityConfigurationOption(#{INTEROPERABILITY_NAME})") if (flag.eql? true)
       retVal << eval("@lifeshield.#{@lifeshield.whereAmI}.clickNodeSettingsSave()")
       @logger.log_message("Save button click in Node settings : #{retVal.last}", LogUtilities::INFO, false)
    rescue
       retVal << false
       @logger.log_message("Something went wrong in the method : #{__method__}", LogUtilities::ERROR, false)
       @logger.log_message("Exception caught: #{$!.inspect}\nError in method #{__method__}", LogUtilities::ERROR)
       @logger.log_message("Exception backtrace:\n #{$!.backtrace.join("\n")}", LogUtilities::DEBUG, false)
    ensure
       @lifeshield.close unless @lifeshield.nil?
       return retVal.present? && retVal.all?
    end
 end
