import os
from argparse import ArgumentParser

import jittor as jt


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--model_dir', default='/home/luck/JDet/swa_ckpt',help='the directory where checkpoints are saved')
    # parser.add_argument(
    #     'starting_model_id',
    #     type=int,
    #     help='the id of the starting checkpoint for averaging, e.g. 1')
    # parser.add_argument(
    #     'ending_model_id',
    #     type=int,
    #     help='the id of the ending checkpoint for averaging, e.g. 12')
    parser.add_argument(
        '--model_ori_name',
        default='model',
        help='the directory for saving the SWA model')
    parser.add_argument(
        '--save_dir',
        default='./',
        help='the directory for saving the SWA model')
    args = parser.parse_args()

    model_dir = args.model_dir
    # starting_id = int(args.starting_model_id)
    # ending_id = int(args.ending_model_id)
    # model_names = list(range(starting_id, ending_id + 1))
    # model_dirs = [
    #     os.path.join(model_dir, 'epoch_' + str(i) + '.pth')
    #     for i in model_names
    # ]
    model_name = args.model_ori_name
    model_paths = [
        os.path.join(model_dir, i)
        for i in os.listdir(model_dir)
    ]
    models = [jt.load(model_path) for model_path in model_paths]
    model_num = len(models)

    model_keys = models[-1]['model'].keys()
    state_dict = models[-1]['model']
    new_state_dict = state_dict.copy()
    ref_model = models[-1]

    for key in model_keys:
        sum_weight = 0.0
        for m in models:
            sum_weight += m['model'][key]
        avg_weight = sum_weight / model_num
        new_state_dict[key] = avg_weight
    ref_model['model'] = new_state_dict
    save_model_name = 'swa_' + model_name + '.pth'
    if args.save_dir is not None:
        save_dir = os.path.join(args.save_dir, save_model_name)
    else:
        save_dir = os.path.join(model_dir, save_model_name)
    jt.save(ref_model, save_dir)
    print('Model is saved at', save_dir)


if __name__ == '__main__':
    main()