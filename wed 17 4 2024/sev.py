def verify_dm_row_greyout():
    retVal = []
    try:
        create_lifeshield_instance()
        retVal.append(mednet_cloud_navigation('deviceList'))
        retVal.append(eval(f"@lifeshield.{@lifeshield.whereAmI}.isRowGrayedOut('{@staticInformation['deviceName']}')"))
        print(f"Is row greyed out in Device List: {retVal[-1]}")
        if not lifeshield.isLoginPageDisplayed():
            retVal.append(lifeshield.logout())
            print(f"Logged out from Lifeshield: {retVal[-1]}")
    except Exception:
        print(f"Something went wrong in the method: {__name__}")
        print(f"Exception caught: {str(sys.exc_info()[1])}\nError in method {__name__}")
        print(f"Exception backtrace:\n {'\n'.join(traceback.format_exception(*sys.exc_info()))}")
    finally:
        if lifeshield is not None:
            lifeshield.close()
        print(f"{__name__} returns: | {bool(retVal) and all(retVal)} |")
        return bool(retVal) and all(retVal)
