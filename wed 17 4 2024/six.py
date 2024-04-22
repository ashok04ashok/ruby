def verify_sw_tooltip(actualSWVersion, expSWVersion):
    result = False
    try:
        i = 0
        swVersion = actualSWVersion.split('-')[0].split('.')
        expVersion = expSWVersion.split('-')[0].split('.')
        for version in swVersion:
            if version > expVersion[i]:
                result = True
                break
            i += 1
    except Exception:
        print(f"Something went wrong in the method: verify_sw_tooltip")
        print(f"Exception caught: {str(sys.exc_info()[1])}\nError in method verify_sw_tooltip")
        print(f"Exception backtrace:\n {'\n'.join(traceback.format_exception(*sys.exc_info()))}")
    finally:
        return result
