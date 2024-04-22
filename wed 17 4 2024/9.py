def set_ivehr_interoperability(flag):
    retVal = []
    text = 'Enable' if flag else 'Disable'
    try:
        print("Login to Customer Account login", LogUtilities.INFO, False)
        create_lifeshield_instance()
        lifeshield.login()
        retVal.append(lifeshield.where_am_i.click_account_configuration())
        retVal.append(lifeshield.where_am_i.select_connectivity_management())
        nodeList = lifeshield.where_am_i.get_column_values('Name')
        print(f"Connectivity Adapter Available : {nodeList}  -- Input CA node name : {NODE_NAME}", LogUtilities.INFO, False)
        nodeIndex = nodeList.index(NODE_NAME)
        print(f"Index of the node {nodeIndex+1} && Node name {NODE_NAME}", LogUtilities.INFO, False)
        retVal.append(lifeshield.where_am_i.select_row_option(nodeIndex+1, 'View Details'))
        retVal.append(lifeshield.where_am_i.click_node_settings_edit())
        print(f"Edit button click in Node settings : {retVal[-1]}", LogUtilities.INFO, False)
        condition = '' if flag else '!'
        retVal.append(lifeshield.where_am_i.enable_interoperability(flag))
        options = lifeshield.where_am_i.get_interoperability_configuration_options() if flag else None
        print(f"Available Configuration Option : {options}", LogUtilities.INFO, False) if flag else None
        retVal.append(lifeshield.where_am_i.select_interoperability_configuration_option(INTEROPERABILITY_NAME)) if flag else None
        retVal.append(lifeshield.where_am_i.click_node_settings_save())
        print(f"Save button click in Node settings : {retVal[-1]}", LogUtilities.INFO, False)
    except Exception as e:
        retVal.append(False)
        print(f"Something went wrong in the method : set_ivehr_interoperability", LogUtilities.ERROR, False)
        print(f"Exception caught: {e}\nError in method set_ivehr_interoperability", LogUtilities.ERROR)
        print(f"Exception backtrace:\n{traceback.format_exc()}", LogUtilities.DEBUG, False)
    finally:
        if lifeshield:
            lifeshield.close()
        return bool(retVal) and all(retVal)
