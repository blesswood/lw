import os
import sys
sys.path.insert(0,f'{os.getcwd()}/lw_configs')
from vw import cfg_dir, user

if not "install" in sys.argv:
    print("Usage:")
    print("   python3 setup.py install")
    print("Before installing:")
    print("   Configure lw_configs/vw.py:")
    print("      Set user to jump between servers")
    print("      Edit masks: mask, mask_restart and mask_config - 4 args for 'mask' and 2 args each for 'mask_restart' and 'mask_config'")
    print("      Set cfg_dir - directory where lw store configs")
    print("      Freq_list_err and freq_list_warn - most common errors and warn in logs to show into 'analize'")
    print("      Component, server, log_file_name, shortnames - servers and shortnames must be with comma, if specified 1 value")
    print("      String 'components_t' must be after each 'component' section")
    print("      \nThanks!")
    sys.exit()

os.system("rm /usr/bin/lw && rm /usr/bin/vw.py && rm /usr/bin/lw.py")

os.system('mkdir {}'.format(cfg_dir))
os.system("chmod 755 -R {}".format(cfg_dir))
os.system("mkdir {}/last_edits".format(cfg_dir))
os.system("touch {}/count_lw.txt".format(cfg_dir))
c = open("{}/count_lw.txt".format(cfg_dir), 'w')
c.write('0')
c.close()

os.system(f"rm {cfg_dir}/vw.py")
os.system("cp lw_configs/vw.py /usr/bin/vw.py && chmod 755 /usr/bin/vw.py".format(cfg_dir,cfg_dir))
os.system("ln -s /usr/bin/vw.py {}/vw.py".format(cfg_dir))

os.system("cp lw.py /usr/bin/")
#os.system("chmod 755 /usr/bin/lw.py")
os.system("chmod +x /usr/bin/lw.py")
os.chdir("/usr/bin")
os.system("ln -s lw.py lw")
os.system("chmod 755 lw")
os.system(f"chown -R {user}:{user} {cfg_dir}")
os.system(f"chmod 755 -R {cfg_dir}")
print("Done")
