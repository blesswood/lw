user = "root"
mask = f'ssh {user}@%s tail -n %s /var/log/%s/%s.log' # %s - server, count_lines, component, log_file_name
mask_config = f'ssh {user}@%s cat /etc/nginx/%s.conf' # server, component
mask_restart = f"ssh {user}@%s sudo systemctl restart %s" # server, component
freq_list_err = [ "failed", "refused"]
freq_list_warn = freq_list_err
cfg_dir = '/etc/lw'


components_t = {}

component = "nginx"
server = "localhost", #ssh section of mask will be erased for localhost
log_file_name = "servername"
shortnames = component,"ngx","ng"
components_t[component] = [server, log_file_name, shortnames]

component = "grafana-server"
server = "192.168.1.52",
log_file_name = "grafana"
shortnames = component,"graf","gf","grfn","gfn"
components_t[component] = [server, log_file_name, shortnames]
