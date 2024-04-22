##cdr_input_hash = {
##    "operationalStatus": "Infusing",
##    "cca": "CCA8",
##    "title": "Program and start Loading dose + Continuous therapy on L1. Note: Post infusion settings set to \"KVO\", NEOI should be set (L1- LOADING DOSE) ",
##    "currentScreen": "MainScreen",
##    "stepNo": 2,
##    "alarmTable": {
##        "deviceList": {},
##        "LEFT_CHANNEL_LINE_1": {},
##        "LEFT_CHANNEL_LINE_2": {},
##        "RIGHT_CHANNEL_LINE_1": {},
##        "RIGHT_CHANNEL_LINE_2": {}
##    },
##    "LEFT_CHANNEL_LINE_1": {
##        "dose": "11 mmol",
##        "doseOrRate": "11 mmol",
##        "doseRate": "N/A",
##        "medication": ["CDR022L1 99 mmol/99.9 mL", False],
##        "infusionStatus": "Infusing",
##        "therapyType": "Loading Dose",
##        "programMode": "Loading Dose",
##        "title": "Program and start Loading dose + Continuous therapy on L1. Note: Post infusion settings set to \"KVO\", NEOI should be set (L1- LOADING DOSE) ",
##        "cca": "CCA8",
##        "clinicalUse": "",
##        "limitAlertsTable": {
##            "1": ["Lower Soft Limit", "Loading Dose Dose", "Lower Soft", "20 mmol", "11 mmol"]
##        },
##        "postInfusion": "kvo",
##        "postInfusionVal": "1",
##        "programmedVolume": "11.1 mL",
##        "programmedDuration": "0 hr 5 min",
##        "deliveryRateRaw": "133.2",
##        "deliveryRate": "133.2 mL/hr",
##        "lineTherapy": "LoadingDose",
##        "currStep": "step-11",
##        "lineStatus": "LOADING DOSE",
##        "currentScreen": "MainScreen"
##    }
##}

##print(cdr_input_hash['line'])

#input={"operationalStatus":"Infusing", "cca":"CCA8", "title":"Program and start Loading dose + Continuous therapy on L1. Note: Post infusion settings set to \\"KVO\\", NEOI should be set (L1- LOADING DOSE) ", "currentScreen":"MainScreen", "stepNo":2, "alarmTable":{"deviceList":{}, "LEFT_CHANNEL_LINE_1":{}, "LEFT_CHANNEL_LINE_2":{}, "RIGHT_CHANNEL_LINE_1":{}, "RIGHT_CHANNEL_LINE_2":{}}, "LEFT_CHANNEL_LINE_1":{"dose":"11 mmol", "doseOrRate":"11 mmol", "doseRate":"N/A", "medication":["CDR022L1 99 mmol/99.9 mL", false], "infusionStatus":"Infusing", "therapyType":"Loading Dose", "programMode":"Loading Dose", "title":"Program and start Loading dose + Continuous therapy on L1. Note: Post infusion settings set to \\"KVO\\", NEOI should be set (L1- LOADING DOSE) ", "cca":"CCA8", "clinicalUse":"", "limitAlertsTable":{"1":["Lower Soft Limit", "Loading Dose Dose", "Lower Soft", "20 mmol", "11 mmol"]}, "postInfusion":"kvo", "postInfusionVal":"1", "programmedVolume":"11.1 mL", "programmedDuration":"0 hr 5 min", "deliveryRateRaw":"133.2", "deliveryRate":"133.2 mL/hr", "lineTherapy":"LoadingDose", "currStep":"step-11", "lineStatus":"LOADING DOSE", "currentScreen":"MainScreen"}
#print(input)
class Lifeshield:
    def __init__(self):
        pass
    
    def isDetailViewDisplayed(self):
        return True
    
    def getProgramDetails(self):
        return {"program_key": "program_value"}
    
    def getDeviceDetails(self):
        return {"device_key": "device_value"}
    
    def getInteroperabilityDetails(self):
        return {"patient_key": "patient_value"}
       

def verify_ai_detailed_view():
##    result = []
##    total_result = []
##    skip_options = IM_DETAILED_PARAMETER_SKIP.copy()
##    program_hash = {}
##    patient_hash = {}
##    device_hash = {}
##    volume_time = {}
##    limit_hash = {}
##    device_dup_hash = {}
##    standby_time = {}
##    periodic_data = None
##    delay_time = None
##    periodic_update = None
##    active_alarm = None
##    time_data = None
##    location_data = None
##   current_page = lifeshield.whereAmI
    line_data = "L1"
##    line_mappings = {v: k for k, v in line_mappings.items()}
##    delay_set = Int.delaySet
##    cancel_delay = Int.cancelDelay
##    skip_linestatus = Int.skipLinestatus
##    post_infusion={line_data:""}

    line_data = "data"

    post_infusion = {"data": None}
    
   
    
    continous_precision_flag={}

    
##    post_infusion={}
    dose_or_rate_post_inf={}
    try:
     print(f"Step-2 : Active Infusions Detailed View Details for L1")
##     @post_infusion[line_data] = false if @post_infusion[line_data].nil?
     if line_data in post_infusion and post_infusion[line_data] is None:
         post_infusion[line_data] = False

     print(post_infusion[line_data])


##     @continous_precision_flag[line_data] = false unless cdr_input_hash['currStep'].eql? @prev_step_executed[line_mappings[line_data]]
     if 2 != 2:
       continous_precision_flag[line_data] = False

       

    
     




     
##        logger.log_message(f"| Is detailedViewDisplayed for {current_page} {line_mappings[line_data]} => {detailed_view_display}|", LogUtilities.INFO, False)
##        ## Is detailedViewDisplayed for activeInfusions LEFT_CHANNEL_LINE_1 => true|
    except Exception as e:
        pass

verify_ai_detailed_view()

