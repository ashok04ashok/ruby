
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
    delayStartMemory={}
    standbyStartMemory={}

    
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
     delayStartMemory[line_data] = None

     if cdr_input_hash['currStep'] != 'step-flush' and delay_start_memory.get(line_data) and cdr_input_hash['infusionStatus'] in ['Infusing', 'Completed']: delayStartMemory[line_data] = True
     print("delayStartMemory :",delayStartMemory)


     
## @standbyStartMemory[lineData]                 = nil if (@standbyStartMemory[lineData].present? && (cdrInputHash['infusionStatus'].exclude? 'Standby'))
     standbyStartMemory[line_data] = None

     if standby_start_memory.get(line_data) and 'Standby' not in cdr_input_hash['infusionStatus']: standbyStartMemory[line_data] = True
     print("standbyStartMemory :",standbyStartMemory)


## actualTherapy = cdrInputHash['lineTherapy']

     actualTherapy = cdr_input_hash.get('lineTherapy')
     print("actualTherapy :",actualTherapy)

         
## @calculationTolerance[lineMappings[lineData]] = cdrInputHash['toleranceUi'] if(cdrInputHash.key? 'toleranceUi')
     calculation_tolerance[line_mappings.get(line_data)] = True  
     print("calculation_tolerance :",calculation_tolerance.get(line_mappings.get(line_data)))


    except Exception as e:
        pass

verify_ai_detailed_view()
