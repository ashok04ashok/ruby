def edit_interoperability_profile(action, profileDetails):
    retVal = []
    try:
        print("Login to Customer Account login", LogUtilities.INFO, False)
        create_lifeshield_instance()
        lifeshield.login()
        retVal.append(lifeshield.where_am_i.click_account_configuration())
        retVal.append(lifeshield.where_am_i.select_interoperability_configuration())
        retVal.append(lifeshield.where_am_i.click_view_details(CONFIGURATION_NAME))
        retVal.append(lifeshield.where_am_i.click_create_new_configuration_version())
        retVal.append(lifeshield.where_am_i.handle_confirmation('Yes'))
        for profile in INTEGRATION_PROFILE:
            if action == 'Add':
                profileDetails['profileType'] = profile
                retVal.append(lifeshield.where_am_i.click_add_profile(profile))
                retVal.append(lifeshield.where_am_i.enter_profile_details(profileDetails))
                retVal.append(lifeshield.where_am_i.click_save_profile(profile))
            elif action == 'Edit':
                profileDetails['profileType'] = profile
                retVal.append(lifeshield.where_am_i.click_edit_profile(profile))
                retVal.append(lifeshield.where_am_i.enter_profile_details(profileDetails))
                retVal.append(lifeshield.where_am_i.click_save_profile(profile))
            elif action == 'Delete':
                retVal.append(lifeshield.where_am_i.click_delete_profile(profile))
                retVal.append(lifeshield.where_am_i.handle_confirmation('Yes'))
            else:
                retVal.append(False)
                print(f"Incorrect Action keyword - {action} given to method {__method__}", LogUtilities.INFO, False)
    except Exception as e:
        retVal.append(False)
        print(f"Something went wrong in the method : {__method__}", LogUtilities.ERROR, False)
        print(f"Exception caught: {e}\nError in method {__method__}", LogUtilities.ERROR)
        print(f"Exception backtrace:\n{traceback.format_exc()}", LogUtilities.DEBUG, False)
    finally:
        lifeshield.where_am_i.click_approve_version()
        lifeshield.close()
        print(f"{__method__} returns: | {bool(retVal) and all(retVal)} |")
        return bool(retVal) and all(retVal)
