# Orchestration script for retraining pipeline
import subprocess
def retrain():
    subprocess.run(['python3','models/trainer.py'], check=True)
    subprocess.run(['python3','models/export_index.py'], check=True)
if __name__=='__main__':
    retrain()
