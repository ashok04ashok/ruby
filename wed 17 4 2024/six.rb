 def self.verify_sw_tooltip(actualSWVersion, expSWVersion)
      expVersion      = []
      result          = false
      i               = 0
      swVersion       = actualSWVersion.split('-')[0].split('.')
      expVersion      = expSWVersion.split('-')[0].split('.')
      swVersion.each do |version|
         if (version > expVersion[i])
            result = true
            break
         end
         i += 1
      end
   rescue
      @logger.log_message("Something went wrong in the method : #{__method__}", LogUtilities::ERROR, false)
      @logger.log_message("Exception caught: #{$!.inspect}\nError in method #{__method__}", LogUtilities::ERROR)
      @logger.log_message("Exception backtrace:\n #{$!.backtrace.join("\n")}", LogUtilities::DEBUG, false)
   ensure
      return result
   end