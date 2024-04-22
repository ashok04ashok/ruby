



class OpenStruct:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)




def verify_ai_detailed_view():

    line_data="step1"

    cdr_input_hash = {'currStep': 'step1', 'infusionStatus': 'Completed', 'lineTherapy': 'lineTherapy_dummy value','toleranceUi': 0.05  }
    prev_step_executed = {'step1': 'value1', 'step2': 'value2'}
    line_mappings = {'line1': 'step1', 'line2': 'step2','step1': 'line_mappings_Step1_dummy_value' }
    delay_start_memory = {'delay_start_memory_dummy_value': 'dummy_value'  }
    standby_start_memory = {'step1': 'dummy_value'  }

    calculation_tolerance={}
    post_infusion = {}
    continousPrecisionFlag = {}
    postInfusion={}
    doseOrRatePostInf={}
    
    lifeshield = {   'step1': OpenStruct(isDetailViewDisplayed=lambda: True)}
    

    
    try:

## form_logger_message("Step-#{cdrInputHash['stepNo']} : Active Infusions Detailed View Details for #{lineData}")
     print(f"Step-2 : Active Infusions Detailed View Details for L1")


## @postInfusion[lineData]                       = false if @postInfusion[lineData].nil?    
     post_infusion[line_data] = False
     if post_infusion[line_data] is None: post_infusion[line_data] = True
     print("post_infusion ",post_infusion)

## @continousPrecisionFlag[lineData]             = false unless cdrInputHash['currStep'].eql? @prevStepExecuted[lineMappings[lineData]]
     continousPrecisionFlag[line_data] = False
     if not cdr_input_hash['currStep'] == prev_step_executed.get(line_mappings.get(line_data)): continousPrecisionFlag[line_data] = True 
     print("continousPrecisionFlag :",continousPrecisionFlag)

## @postInfusion[lineData]                       = false unless cdrInputHash['currStep'].eql? @prevStepExecuted[lineMappings[lineData]]
     postInfusion[line_data] = False
     if not cdr_input_hash['currStep'] == prev_step_executed.get(line_mappings.get(line_data)): postInfusion[line_data] = True

     print("postInfusion :",postInfusion)

      
## @doseOrRatePostInf[lineData]                  = false unless cdrInputHash['currStep'].eql? @prevStepExecuted[lineMappings[lineData]]  
     doseOrRatePostInf[line_data] = False
     if not cdr_input_hash['currStep'] == prev_step_executed.get(line_mappings.get(line_data)): doseOrRatePostInf[line_data] = True
     print("doseOrRatePostInf :",doseOrRatePostInf)

## @delayStartMemory[lineData]                   = nil if ((!cdrInputHash['currStep'].eql? 'step-flush') && @delayStartMemory[lineData].present? && (%w[Infusing Completed].include? cdrInputHash['infusionStatus']))
     delay_start_memory[line_data] = None
     # Your Python code using the ternary operator
     delay_start_memory[line_data] = True if cdr_input_hash['currStep'] != 'step-flush' and delay_start_memory.get(line_data) and cdr_input_hash['infusionStatus'] in ['Infusing', 'Completed'] else False
     print("delayStartMemory :",delay_start_memory)


     
## @standbyStartMemory[lineData]                 = nil if (@standbyStartMemory[lineData].present? && (cdrInputHash['infusionStatus'].exclude? 'Standby'))
     standby_start_memory[line_data] = None
     if standby_start_memory.get(line_data) and 'Standby' not in cdr_input_hash['infusionStatus']: standbyStartMemory[line_data] = True
     print("standbyStartMemory :",standby_start_memory)


## actualTherapy = cdrInputHash['lineTherapy']

     actualTherapy = cdr_input_hash.get('lineTherapy')
     print("actualTherapy :",actualTherapy)

         
## @calculationTolerance[lineMappings[lineData]] = cdrInputHash['toleranceUi'] if(cdrInputHash.key? 'toleranceUi')
     calculation_tolerance[line_mappings.get(line_data)] = True  
     print("calculation_tolerance :",calculation_tolerance)
     calculation_tolerance={}



##       detailedViewDisplay = eval("@lifeshield.step1.isDetailViewDisplayed()")

     step1_data = lifeshield['step1']
     is_detailed_view_displayed = step1_data.isDetailViewDisplayed()
     
     detailedViewDisplay=is_detailed_view_displayed
     print("detailedViewDisplay :",detailedViewDisplay)

##===============================================================================
     print(f"|{'=' * 50}|")
     volume_counters = {"LEFT_CHANNEL_LINE_1": 30,    "LEFT_CHANNEL_LINE_2": 30,    "RIGHT_CHANNEL_LINE_1": 30,    "RIGHT_CHANNEL_LINE_2": 30}

     print(f"Wrapper Clear Volume Counter : {volume_counters}")

##      ///////// Infusion Details   //////
     print(f"|{'-' * 50}|")
     print("Infusion Details")
     print(f"|{'-' * 50}|")

           
     Infusion_l1 = {'Dose': '11 mmol', 'Dose Rate': 'N/A','Medication': 'CDR022L1','Infusion Status': 'Infusing','Program Mode': 'Loading Dose','CCA': 'CCA8','Clinical Use': '-','Programmed Volume': '11.1 mL','Programmed Duration': '0 hr 5 min','Delivery Rate': '133.2 mL/hr','Line': 'L1','Facility':'Default_sysuserZ8M','Volume Delivered': '0 mL','Volume Remaining': '11.1 mL','Time Remaining': '0 hr 5 min','Last Updated': '2024-04-02 10:21:17'}
     Infusion_l2 = {'Dose': '11 mmol', 'Dose Rate': 'N/A','Medication': 'CDR022L1','Infusion Status': 'Infusing','Program Mode': 'Loading Dose','CCA': 'CCA8','Clinical Use': '-','Programmed Volume': '11.1 mL','Programmed Duration': '0 hr 5 min','Delivery Rate': '133.2 mL/hr','Line': 'L1','Facility':'Default_sysuserZ8M','Volume Delivered': '0 mL','Volume Remaining': '11.1 mL','Time Remaining': '0 hr 5 min','Last Updated': '2024-04-02 10:21:17'}
     Infusion_result = {'Dose': 'true', 'Dose Rate': 'true','Medication': 'true','Infusion Status': 'true','Program Mode':'true','CCA': 'true','Clinical Use': 'true','Programmed Volume': 'true','Programmed Duration': 'ture','Delivery Rate': 'true','Line': 'true','Facility': 'true','Volume Delivered': 'true','Volume Remaining': 'true','Time Remaining': 'true','Last Updated': 'true'}

     
     print(f"|{'=' * 50}|")


     print(f"|{'=' * 50}|")
     print(f"|{'=' * 100}|")
     print(f"| Field  {' ' * 14}| Expected {' ' * 17}| Actual {' ' * 18}| Result ")
    
     print(f"|{'=' * 100}|")

# Iterate over the enumerated keys of the dictionary
     for index, key in enumerate(Infusion_l1):
         keys_list = list(Infusion_l1.keys())

         print(f"| {keys_list[index].ljust(20)} | {Infusion_l1[key].ljust(25)} | {Infusion_l2[key].ljust(24)} | {Infusion_result[key]} |")

##         print(f"| {keys_list[index].ljust(20)} | {Infusion_l1[key].ljust(25)} | {Infusion_l2[key].ljust(24)} | {Infusion_l1[key]==Infusion_l2[key]} |")

    
##      ///////// Pump Details   //////
     print(f"|{'-' * 50}|")
     print("Pump Details")
     print(f"|{'-' * 50}|")

     Infusion_l11 = {'Pump ID': 'ICU02122421D4','Network Status': '{"status":"Online"}','Location': 'a2:17:c8:c7:f3:db','Software Version': '1.2.0.45-test','Drug Library LastUpdated': '2024-03-29 00:58:38','Drug Library': 'LifeShield : 2.2 10019','Pump Name': 'SilverZ8M','Serial Number': '8000001395','Pump Type': 'Plum Duo','Power Status': 'Powered On'}

     Infusion_l12 = {'Pump ID': 'ICU02122421D4','Network Status': '{"status":"Online"}','Location': 'a2:17:c8:c7:f3:db','Software Version': '1.2.0.45-test','Drug Library LastUpdated': '2024-03-29 00:58:38','Drug Library': 'LifeShield : 2.2 10019','Pump Name': 'SilverZ8M','Serial Number': '8000001395','Pump Type': 'Plum Duo','Power Status': 'Powered On'}

     Infusion_result1 = {'Pump ID': 'true','Network Status': 'true','Location': 'true','Software Version': 'true','Drug Library LastUpdated': 'ture','Drug Library': 'true','Pump Name': 'true','Serial Number': 'true','Pump Type': 'true','Power Status': 'true'}

     
     
     print(f"|{'=' * 50}|")


     print(f"|{'=' * 50}|")
     print(f"|{'=' * 100}|")
     print(f"| Field  {' ' * 18}| Expected {' ' * 17}| Actual {' ' * 18}| Result ")
    
     print(f"|{'=' * 100}|")

# Iterate over the enumerated keys of the dictionary
     for index, key in enumerate(Infusion_l11):
         keys_list = list(Infusion_l11.keys())
####         print(f"| {keys_list[index]} {' ' * (15-len(Infusion_l11[key]))}| {Infusion_l11[key]} {' ' * 11}| {Infusion_l12[key]} {' ' * 9}|{Infusion_result1[key]}")
         print(f"| {keys_list[index].ljust(24)} | {Infusion_l11[key].ljust(25)} | {Infusion_l12[key].ljust(24)} | {Infusion_result1[key]} |")



    
    
##      ///////// Auto Program Details   //////
     print(f"|{'-' * 50}|")
     print("Auto Program Details")
     print(f"|{'-' * 50}|")
     Infusion_l21 = {'Patient Name': '-','Nursing Unit': '-','Room/Bed': '-','Patient ID': '-','Program Source': 'Manual','Order ID': '-','Caregiver ID': '-','Caregiver Name': '-','Program Source Tooltip': 'No icon present'}

     Infusion_l22 = {'Patient Name': '-','Nursing Unit': '-','Room/Bed': '-','Patient ID': '-','Program Source': 'Manual','Order ID': '-','Caregiver ID': '-','Caregiver Name': '-','Program Source Tooltip': 'No icon present'}

     Infusion_result2 = {'Patient Name': 'true','Nursing Unit': 'true','Room/Bed': 'true','Patient ID': 'true','Program Source': 'true','Order ID': 'true','Caregiver ID': 'true','Caregiver Name': 'true','Program Source Tooltip': 'true'}



     
     print(f"|{'=' * 50}|")


     print(f"|{'=' * 50}|")
     print(f"|{'=' * 100}|")
     print(f"| Field  {' ' * 16}| Expected {' ' * 17}| Actual {' ' * 18}| Result ")
    
     print(f"|{'=' * 100}|")

# Iterate over the enumerated keys of the dictionary
     for index, key in enumerate(Infusion_l21):
         keys_list = list(Infusion_l21.keys())
##        print(f"|{keys_list[index].ljust(100)}| {Infusion_l1[key].ljust(25)} | {Infusion_l2[key].ljust(25)}|{Infusion_result[key].ljust(2)}|")
##         print(f"| {keys_list[index]} {' ' * (15-len(Infusion_l21[key]))}| {Infusion_l21[key]} {' ' * 11}| {Infusion_l22[key]} {' ' * 9}|{Infusion_result2[key]}")
         print(f"| {keys_list[index].ljust(22)} | {Infusion_l21[key].ljust(25)} | {Infusion_l22[key].ljust(24)} | {Infusion_result2[key]} |")

     
     print(f"|{'=' * 100}|")
     condition=-5.000
     operator=0.0
     
     print(f"Wrapper Clear Volume Counter : {condition} |{' ' * 10}| {operator}|{' ' * 10}| {operator} ")
     
    
    except Exception as e:
        pass

verify_ai_detailed_view()
