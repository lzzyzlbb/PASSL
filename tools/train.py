# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)

from passl.utils.options import parse_args
from passl.utils.config import get_config
from passl.utils.setup import setup
from passl.engine.trainer import Trainer
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def main(args, cfg):
    # init environment, include logger, dynamic graph, seed, device, train or test mode...
    setup(args, cfg)
    # build trainer
    trainer = Trainer(cfg)

    # continue train or evaluate, checkpoint need contain epoch and optimizer info
    if args.resume:
        trainer.resume(args.resume)
    # evaluate or finute, only load generator weights
    elif args.load:
        trainer.load(args.load)

    if args.evaluate_only:
        trainer.val()
        return

    trainer.train()


if __name__ == '__main__':
    args = parse_args()
    cfg = get_config(args.config_file)
    main(args, cfg)
