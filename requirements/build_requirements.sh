pip-compile --upgrade --output-file=dev.txt in/common.in in/communicator.in in/dev.in in/worker.in
pip-compile --upgrade --output-file=communicator.txt in/common.in in/communicator.in
pip-compile --upgrade --output-file=worker.txt in/common.in in/worker.in
