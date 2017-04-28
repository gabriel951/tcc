# python file that contain the function to remove from the code the outliers

# outliers dictionary 
outliers_dict = {}

def register_outliers_low_pass_rate(stu_info):
    """
    registers student that were not interessed in coursing any subject in unb 
    receives: 
        student dictionary 
    returns: 
        nothing
    * all cases were analysed manually, that's why this function is so messy and big
    """
    global outliers_dict

    # get outliers list
    outliers_dict[14716420102] = 14716420102
    outliers_dict[12392620062] = 12392620062
    outliers_dict[16534020131] = 16534020131
    outliers_dict[7053820001] = 7053820001
    outliers_dict[7776420011] = 7776420011
    outliers_dict[17265320111] = 17265320111
    outliers_dict[18212520112] = 18212520112
    outliers_dict[23120820151] = 23120820151
    outliers_dict[19037520121] = 19037520121
    outliers_dict[16685220102] = 16685220102
    outliers_dict[18758820121] = 18758820121
    outliers_dict[17302520111] = 17302520111
    outliers_dict[20738720132] = 20738720132
    outliers_dict[11147420051] = 11147420051
    outliers_dict[12379120062] = 12379120062
    outliers_dict[16139420101] = 16139420101
    outliers_dict[21745820141] = 21745820141
    outliers_dict[14767120102] = 14767120102
    outliers_dict[11872920061] = 11872920061
    outliers_dict[10701120042] = 10701120042
    outliers_dict[21342020141] = 21342020141
    outliers_dict[15408620092] = 15408620092
    outliers_dict[9936020032] = 9936020032
    outliers_dict[18045420112] = 18045420112
    outliers_dict[22218220142] = 22218220142
    outliers_dict[18901220121] = 18901220121
    outliers_dict[7092020002] = 7092020002
    outliers_dict[15645320092] = 15645320092
    outliers_dict[16518620102] = 16518620102
    outliers_dict[8232920012] = 8232920012
    outliers_dict[18054620112] = 18054620112
    outliers_dict[24374920161] = 24374920161
    outliers_dict[21564120141] = 21564120141
    outliers_dict[19875120131] = 19875120131
    outliers_dict[17369220111] = 17369220111
    outliers_dict[13176620072] = 13176620072
    outliers_dict[15403820092] = 15403820092
    outliers_dict[16106720101] = 16106720101
    outliers_dict[22495020142] = 22495020142
    outliers_dict[18760320121] = 18760320121
    outliers_dict[23905920152] = 23905920152
    outliers_dict[20120020131] = 20120020131
    outliers_dict[22449620142] = 22449620142
    outliers_dict[7059220002] = 7059220002
    outliers_dict[19281020122] = 19281020122
    outliers_dict[21610620141] = 21610620141
    outliers_dict[8822220021] = 8822220021
    outliers_dict[20871120132] = 20871120132
    outliers_dict[23789520152] = 23789520152
    outliers_dict[17708320111] = 17708320111
    outliers_dict[12240320062] = 12240320062
    outliers_dict[23041820151] = 23041820151
    outliers_dict[8800020021] = 8800020021
    outliers_dict[18667820121] = 18667820121
    outliers_dict[13977020081] = 13977020081
    outliers_dict[9377720031] = 9377720031
    outliers_dict[21355620141] = 21355620141
    outliers_dict[14809620091] = 14809620091
    outliers_dict[21486520141] = 21486520141
    outliers_dict[9645320031] = 9645320031
    outliers_dict[21463820141] = 21463820141
    outliers_dict[17149020111] = 17149020111
    outliers_dict[23802120152] = 23802120152
    outliers_dict[22320220142] = 22320220142
    outliers_dict[22118320142] = 22118320142
    outliers_dict[11477420052] = 11477420052
    outliers_dict[6966820001] = 6966820001
    outliers_dict[11938520061] = 11938520061
    outliers_dict[19285420122] = 19285420122
    outliers_dict[19683920122] = 19683920122
    outliers_dict[13221620072] = 13221620072
    outliers_dict[14271220082] = 14271220082
    outliers_dict[24457120161] = 24457120161
    outliers_dict[12491420062] = 12491420062
    outliers_dict[13998320081] = 13998320081
    outliers_dict[13877120081] = 13877120081
    outliers_dict[12570520071] = 12570520071
    outliers_dict[8454720012] = 8454720012
    outliers_dict[21713620141] = 21713620141
    outliers_dict[18296420112] = 18296420112
    outliers_dict[7903120011] = 7903120011
    outliers_dict[18254720112] = 18254720112
    outliers_dict[12375820062] = 12375820062
    outliers_dict[16709520102] = 16709520102
    outliers_dict[8369220012] = 8369220012
    outliers_dict[11447620052] = 11447620052
    outliers_dict[14414720082] = 14414720082
    outliers_dict[21573520141] = 21573520141
    outliers_dict[13412420072] = 13412420072
    outliers_dict[16132320101] = 16132320101
    outliers_dict[23173520151] = 23173520151
    outliers_dict[7110020002] = 7110020002
    outliers_dict[15347420111] = 15347420111
    outliers_dict[23181020151] = 23181020151
    outliers_dict[13973720081] = 13973720081
    outliers_dict[16072020101] = 16072020101
    outliers_dict[11388120121] = 11388120121
    outliers_dict[23167020151] = 23167020151
    outliers_dict[20699020132] = 20699020132
    outliers_dict[15903220101] = 15903220101
    outliers_dict[22177320142] = 22177320142
    outliers_dict[16755920102] = 16755920102
    outliers_dict[18215120112] = 18215120112
    outliers_dict[14899020091] = 14899020091
    outliers_dict[22720720150] = 22720720150
    outliers_dict[19386520122] = 19386520122
    outliers_dict[22857420151] = 22857420151
    outliers_dict[13320220072] = 13320220072
    outliers_dict[18596720121] = 18596720121
    outliers_dict[6988820001] = 6988820001
    outliers_dict[9216020022] = 9216020022
    outliers_dict[8809320021] = 8809320021
    outliers_dict[10447720041] = 10447720041
    outliers_dict[12239720062] = 12239720062
    outliers_dict[23168020151] = 23168020151
    outliers_dict[15519420092] = 15519420092
    outliers_dict[24371220161] = 24371220161
    outliers_dict[10345820041] = 10345820041
    outliers_dict[8329220012] = 8329220012
    outliers_dict[18726320121] = 18726320121
    outliers_dict[20716720132] = 20716720132
    outliers_dict[11668820052] = 11668820052
    outliers_dict[11191120101] = 11191120101
    outliers_dict[23206220151] = 23206220151
    outliers_dict[24435020161] = 24435020161
    outliers_dict[17708020111] = 17708020111
    outliers_dict[7047320001] = 7047320001
    outliers_dict[23113020151] = 23113020151
    outliers_dict[15374820092] = 15374820092
    outliers_dict[14295020082] = 14295020082
    outliers_dict[11149120051] = 11149120051
    outliers_dict[22942020151] = 22942020151
    outliers_dict[6987920001] = 6987920001
    outliers_dict[23179920151] = 23179920151
    outliers_dict[24384320161] = 24384320161
    outliers_dict[13922620081] = 13922620081
    outliers_dict[23952020152] = 23952020152
    outliers_dict[23906620152] = 23906620152
    outliers_dict[20331320131] = 20331320131
    outliers_dict[16138720101] = 16138720101
    outliers_dict[9647920031] = 9647920031
    outliers_dict[14826920091] = 14826920091
    outliers_dict[23850120152] = 23850120152
    outliers_dict[20348720131] = 20348720131
    outliers_dict[14958720091] = 14958720091
    outliers_dict[21663020141] = 21663020141
    outliers_dict[15628120092] = 15628120092
    outliers_dict[8402720012] = 8402720012
    outliers_dict[21882320141] = 21882320141
    outliers_dict[8738420021] = 8738420021
    outliers_dict[20562720132] = 20562720132
    outliers_dict[16170120101] = 16170120101
    outliers_dict[21512820141] = 21512820141
    outliers_dict[11022620092] = 11022620092
    outliers_dict[17610520111] = 17610520111
    outliers_dict[22858520151] = 22858520151
    outliers_dict[9100220022] = 9100220022
    outliers_dict[17348020111] = 17348020111
    outliers_dict[18028820112] = 18028820112
    outliers_dict[18293420112] = 18293420112
    outliers_dict[21496420141] = 21496420141
    outliers_dict[7715420011] = 7715420011
    outliers_dict[19354720122] = 19354720122
    outliers_dict[20276320131] = 20276320131
    outliers_dict[21801220141] = 21801220141
    outliers_dict[19323820122] = 19323820122
    outliers_dict[9962920032] = 9962920032
    outliers_dict[10792520042] = 10792520042
    outliers_dict[14289320082] = 14289320082
    outliers_dict[15478920092] = 15478920092
    outliers_dict[23818320152] = 23818320152
    outliers_dict[23181220151] = 23181220151
    outliers_dict[23565220152] = 23565220152
    outliers_dict[23129220151] = 23129220151
    outliers_dict[23110220151] = 23110220151
    outliers_dict[20922620132] = 20922620132
    outliers_dict[16869620102] = 16869620102
    outliers_dict[14005320081] = 14005320081
    outliers_dict[14073920081] = 14073920081
    outliers_dict[9116220022] = 9116220022
    outliers_dict[13212220082] = 13212220082
    outliers_dict[11525520052] = 11525520052
    outliers_dict[22066920142] = 22066920142
    outliers_dict[24729320161] = 24729320161
    outliers_dict[9588620031] = 9588620031
    outliers_dict[21611920141] = 21611920141
    outliers_dict[22175120142] = 22175120142
    outliers_dict[23537720152] = 23537720152
    outliers_dict[16122420112] = 16122420112
    outliers_dict[20326420131] = 20326420131
    outliers_dict[12774620071] = 12774620071
    outliers_dict[21785820141] = 21785820141
    outliers_dict[12607020071] = 12607020071
    outliers_dict[22969220151] = 22969220151
    outliers_dict[14939520091] = 14939520091
    outliers_dict[20131120131] = 20131120131
    outliers_dict[18193620112] = 18193620112
    outliers_dict[17710120111] = 17710120111
    outliers_dict[11469320052] = 11469320052
    outliers_dict[22525820142] = 22525820142
    outliers_dict[11133220051] = 11133220051
    outliers_dict[24471420161] = 24471420161
    outliers_dict[7080820002] = 7080820002
    outliers_dict[12179120061] = 12179120061
    outliers_dict[10803320042] = 10803320042
    outliers_dict[8327020012] = 8327020012
    outliers_dict[13191020072] = 13191020072
    outliers_dict[21505220141] = 21505220141
    outliers_dict[23434420151] = 23434420151
    outliers_dict[11729720061] = 11729720061
    outliers_dict[21471420141] = 21471420141
    outliers_dict[21715520141] = 21715520141
    outliers_dict[8439420012] = 8439420012
    outliers_dict[19639820122] = 19639820122
    outliers_dict[10867720051] = 10867720051
    outliers_dict[20973920132] = 20973920132
    outliers_dict[23161920151] = 23161920151
    outliers_dict[10003120032] = 10003120032
    outliers_dict[24481120161] = 24481120161
    outliers_dict[23024820151] = 23024820151
    outliers_dict[22515720142] = 22515720142
    outliers_dict[19039920121] = 19039920121
    outliers_dict[9150020022] = 9150020022
    outliers_dict[12025920061] = 12025920061

def register_outliers_death(stu_info):
    """
    registers student that died
    receives: 
        student dictionary 
    returns: 
        nothing
    """
    global outliers_dict

    # outliers
    outliers_dict[20948320132] = 20948320132
    outliers_dict[10832120042] = 10832120042
    outliers_dict[12233520062] = 12233520062
    outliers_dict[16526220102] = 16526220102
    outliers_dict[23137120151] = 23137120151
    outliers_dict[20685820132] = 20685820132

def handle_outliers(stu_info):
    """
    eliminates students outliers
    receives: 
        1. student dictionary
    returns: 
        nothing
    """
    global outliers_dict

    # register as outliers students that left because they died
    register_outliers_death(stu_info)

    # register outliers that did not pass in any subjects
    register_outliers_low_pass_rate(stu_info)
    
    # eliminate outliers
    for outlier in outliers_dict: 
        try: 
            del stu_info[outlier]
        except KeyError:
            pass

    print('finishing handling outliers')
