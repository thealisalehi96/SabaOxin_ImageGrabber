import os
from pathlib import Path


def get_last_floder_name(dir_name, folder_name = 'plate', defect_deteection_algo=False):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


    try:

        if len(next(os.walk(dir_name))[1]) != 0:

            last_created_folder = sorted(Path(dir_name).iterdir(), key=os.path.getmtime)[-1].as_posix()
            last_itr = int(last_created_folder.split('_')[-1]) + 1

        else:
            last_itr = 1

        #print(last_itr)
        if not defect_deteection_algo:
            os.makedirs(os.path.join(dir_name , str(folder_name+'_'+str(last_itr))))
            folder_path = os.path.join(dir_name , str(folder_name+'_'+str(last_itr)))
            return folder_path
        else:
            os.makedirs(os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'perfect'))
            os.makedirs(os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'defect'))
            perfect_folder_path = os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'perfect')
            defect_folder_path = os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'defect')
            return perfect_folder_path, defect_folder_path
    
    except:
        print('here')
        last_itr = len(next(os.walk(dir_name))[1]) + 1
        while os.path.exists(os.path.join(dir_name , str(folder_name+'_'+str(last_itr)))):
            last_itr += 1
        
        if not defect_deteection_algo:
            os.makedirs(os.path.join(dir_name , str(folder_name+'_'+str(last_itr))))
            folder_path = os.path.join(dir_name , str(folder_name+'_'+str(last_itr)))
            return folder_path
        else:
            os.makedirs(os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'perfect'))
            os.makedirs(os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'defect'))
            perfect_folder_path = os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'perfect')
            defect_folder_path = os.path.join(dir_name , str(folder_name+'_'+str(last_itr)), 'defect')
            return perfect_folder_path, defect_folder_path





if __name__ == "__main__":
    
    print(get_last_floder_name(dir_name='save_path', dir_name_alt='save_path_alt', folder_name = 'plate'))



