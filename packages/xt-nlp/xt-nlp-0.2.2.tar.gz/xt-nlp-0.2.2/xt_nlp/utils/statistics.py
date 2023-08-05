import math
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def print_example_stats(examples, do_all_perms):
    """# prints information about examples.
    The following information is # printed:
    - total number of examples
    - total number of examples with no answers
    - total number of ans_types
    - if do_all_perms is true: 
        for each combination of ans_types, # print the total number of examples matching the combination

    Agruments:
        'examples': 
            a list of SESExamples
        'do_all_perms':
            boolean to control # print output (see above)
    """

    logging.info("Number of Examples: " +str(len(examples)))
    all_ans_types = []
    total_empty = 0
    for e in examples:
        if len(e.ans_list) == 0:
                total_empty += 1 
        for ans in e.ans_list:
            if ans.ans_type not in all_ans_types:
                all_ans_types.append(ans.ans_type)
    logging.info("Number of empty examples: " + str(total_empty))
    logging.info("Number of ans_types: " + str(len(all_ans_types)))
    
    if do_all_perms:
        for l in range(len(all_ans_types)+1):
            for s in itertools.combinations(all_ans_types, l):
                total = 0
                for e in examples:
                    ex_ans = [ans.ans_type for ans in e.ans_list]
                    total += 1
                    for s_an in s:
                        if s_an not in ex_ans:
                            total -=1
                            break
                logging.info(str(s) + " -- count: " + str(total))

def print_feature_stats(features, ans_types, do_all_perms):
    """# prints information about features.
    The following information is # printed:
    - total number of features
    - the size of the start_position in the first element of features
    - the size of the end_position in the first element of features
    - total number of features with no answers
    - if do_all_perms is true: 
        for each combination of ans_types, # print the total number of features matching the combination
    - for each ans_type, # print the number of ans in all features

    Agruments:
        'examples': 
            a list of SESExamples
        'ans_types':
            list of all ans_types
        'do_all_perms':
            boolean to control # print output (see above)
    """

    logging.info("Number of features: " +str(len(features)))
    if len(features) == 0:
        logging.info("No features found. Returning")
        return
    logging.info("size of start: " + str(len(features[0].start_position)))
    logging.info("size of end: " + str(len(features[0].end_position)))
    
    total_full_empty = 0
    for f in features:
        total_full_empty += 1
        for impossible in f.is_impossible:
            if not impossible:
                total_full_empty -= 1
                break
    logging.info("Number of full impossible: " + str(total_full_empty))
    
    if do_all_perms:
        for l in range(len(all_ans_types)+1):
            for s in itertools.combinations(ans_types, l):
                total = 0
                for f in features:
                    total += 1
                    for s_an in s:
                        index = ans_types.index(s_an)
                        if f.is_impossible[index]:
                            total -= 1
                            break    
                logging.info(str(s) + " **** feature count: " + str(total))

    for i, ans in enumerate(ans_types):
        total_ans = 0
        
        for f in features:
            if not f.is_impossible[i]:
                total_ans += len(f.start_position[i])

        logging.info("# ans: " + str(ans) + " = " + str(total_ans))
