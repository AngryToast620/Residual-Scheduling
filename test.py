import torch
import copy
from params import get_args
from env.env import JSP_Env
from model.REINFORCE import REINFORCE
import time
import os
from heuristic import *

def test():
    for instance in os.listdir(args.test_dir):
        file = os.path.join(args.test_dir, instance)
        path = file.replace('\\ta', '/ta')
        for i in range(1000):
            avai_ops = env.load_instance(file)
            st = time.time()

            # heuristic rule
            ##
            MWKR_ms = heuristic_makespan(copy.deepcopy(env), copy.deepcopy(avai_ops), args.rule)
            ##

            while True:
                data, op_unfinished= env.get_graph_data()
                action_idx, action_prob = policy(avai_ops, data, op_unfinished, env.jsp_instance.graph.max_process_time, greedy=False, tempature=0.05)   # greedy=True to use the best selection, if we want to generate different result, greedy=False
                avai_ops, _, done = env.step(avai_ops[action_idx])
                
                if done:
                    ed = time.time()
                    policy.clear_memory()

                    print("instance : {}, ms : {}, time : {}".format(path, env.get_makespan(), ed - st))
                    with open("./result/{}/test_result_T=0.05.txt".format(args.date),"a") as outfile:
                        outfile.write(f'instance : {path:60}, policy : {env.get_makespan():10}\t')
                        outfile.write(f'time : {ed - st:10}\n')
                    break


        # # heuristic rule
        # ##
        # avai_ops = env.load_instance(file)
        # st = time.time()
        # MWKR_ms = heuristic_makespan(copy.deepcopy(env), copy.deepcopy(avai_ops), args.rule)
        # ed = time.time()
        # print("instance : {}, ms : {}, time : {}".format(file, MWKR_ms, ed - st))
        # with open("./result/mwkr/mwkr_test_result.txt","a") as outfile:
        #     outfile.write(f'instance : {file:60}, policy : {MWKR_ms:10}\t')
        #     outfile.write(f'time : {ed - st:10}\n')
        # ##


if __name__ == '__main__':
    args = get_args()
    print(args)
    env = JSP_Env(args)
    policy = REINFORCE(args).to(args.device)
    os.makedirs('./result/{}/'.format(args.date), exist_ok=True)
    
    policy.load_state_dict(torch.load(args.load_weight, map_location=args.device), False)
    with torch.no_grad():
        test()
                    