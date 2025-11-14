def clean_data(value:str):
    requirement = ["SAT","GRE","GMAT","ACT","ATAR","GPA","TOEFL","IELTS"]
    haveMaster = False
    haveBachelor = False
    Bachelor_requirement = {
        "SAT": None,
        "GRE": None,
        "GMAT": None,
        "ACT": None,
        "ATAR" :None,
        "GPA":None,
        "TOEFL": None,
        "IELTS": None
    }
    Master_requirement = {
        "SAT": None,
        "GRE": None,
        "GMAT": None,
        "ACT": None,
        "ATAR" :None,
        "GPA":None,
        "TOEFL": None,
        "IELTS": None
    }
    # Bachelor = ["Bachelor","General"]
    # Master = ["Master"]
    Master_infor = [x.strip() for x in value.split("Master") if "+" in x]
    # print(Master_infor)
    if len(Master_infor)>1:
        haveMaster = True
        Master_infor = Master_infor[1].strip().split()
        for data_index in range(len(Master_infor)-1):
            if Master_infor[data_index] in requirement:
                # print(Master_infor[data_index])
                Master_requirement[Master_infor[data_index]] = Master_infor[data_index+1] 
    
    Bachelor_infor = value.split("Master")[0].strip()
    Bachelor_infor = [x.strip() for first_split in Bachelor_infor.split("Bachelor") for x in first_split.split("General") if "+" in x and "email" not in x]
    
    # print(Bachelor_infor)
    
    Bachelor_infor = Bachelor_infor[0]
    if Bachelor_infor:
        haveBachelor = True
        Bachelor_infor = Bachelor_infor.split()
        for data_index in range(len(Bachelor_infor)-1):
            if Bachelor_infor[data_index] in requirement:
                Bachelor_requirement[Bachelor_infor[data_index]] = Bachelor_infor[data_index+1] 
    return haveBachelor, Bachelor_requirement, haveMaster, Master_requirement

# data = 'University information Admission Bachelor SAT 1520+ TOEFL 100+ Master GMAT 728+ IELTS 7+ TOEFL 90+ Students & Staff Total students 11,720 UG students 39% PG students 61% International students 3,824 UG students 17% PG students 83% Total faculty staff 3,134 Domestic staff 43% Int\'l staff 57%'
# haveBachelor, Bachelor_infor, haveMaster, Master_infor = clean_data(data)
# print(Bachelor_infor)
# print(Master_infor)


# data = 'University information Admission [email protected] | +44 (0)20 3370 1215 [email protected] | +44 (0)20 3108 7288 General GPA 3.5+ GRE 322+ GMAT 600+ ACT 32+ SAT 1490+ ATAR 96+ International Baccalaureate 39+ PTE Academic 62+ Cambridge CAE Advanced 176+ TOEFL 92+ IELTS 6.5+ Master GMAT 600+ GRE 260+ GPA 2.7+ IELTS 6.5+ TOEFL 92+ Facilities Academic resources A number of resources to help you with your studies including libraries, museums and UCL\'s Centre for Languages & International Education (CLIE). Entertainment Relax on campus in your free time by visiting the Bloomsbury Theatre, going to a gig at the Students\' Union, or learning something new at one of UCL\'s museums. Contemplation facilities UCL is a secular institution and has a contemplation room on-site for private meditation and prayer. Students & Staff Total students 45,530 UG students 54% PG students 46% International students 25,672 UG students 51% PG students 49% Total faculty staff 7,533 Domestic staff 53% Int\'l staff 47% Student life Teaching and Learning Research-based learning: A UCL education At UCL, our students get the chance to carry out research of their own, and have a say in decisions affecting their education. Life skills Learn how UCL\'s teaching can help you develop your academic and life skills. Global citizenship A two-week summer programme aimed at broadening students\' experiences for life after graduation. Study abroad Get an international perspective by studying abroad as part of your undergraduate degree programme. Work and department placements Broaden your experience through a work placement or take part in a summer research programme. Clubs, societies and volunteering Students\' Union Students\' Union UCL runs over 200 clubs and societies giving students the opportunity to participate in sports activities, attend events or volunteer through the Volunteering Service. Student Ambassadors UCL students can help at UCL events, giving tours and presentations, by becoming a Student Ambassador. School and college partnerships Further opportunities to volunteer. Support and Welfare Support and wellbeing UCL offers a number of support and health services to all students including a day nursery, health centre and facilities for those with disabilities. International students Support is available to international students before and after arriving at UCL through immigration advice and the International Students\' Orientation Programme.'

# haveBachelor, Bachelor_infor, haveMaster, Master_infor = clean_data(data)
# print(Bachelor_infor)
# print(Master_infor)