
def create_lifeshield_instance():
    print ("navigate  create_lifeshield_instance page")
    pass


class Int:
    @staticmethod
    def handle_alarm():
        return False


# Define the method
def publish_software(software, screen):
    retVal = []
    try:
     retVal.append(True)
      
    except Exception:
        print("Exception")
        retVal.append(False)
        if retVal[-1] is False:
            Int.lifeshield_screen_capture("DL creation issue")
        print("Something went wrong in the method : create_or_edit_drug_library")
        print(
            "Exception caught: {}\nError in method create_or_edit_drug_library".format(
                str(sys.exc_info()[1])
            )
        )
        print("Exception backtrace:\n{}".format(traceback.format_exc()))

    finally:
        print("finally")
        dlFailedFlag = None
        if screen not in ['PowerOff', 'BiomedScreen']:
            Int.handle_alarm = True
        print("handle_alarm returns: | {} |".format( retVal is not None and all(retVal)))
          # lifeshield.logout()
        return retVal is not None and all(retVal)
        
        

publish_software(software=True, screen="SomeScreen")

