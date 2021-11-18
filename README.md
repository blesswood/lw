# lw
### Log vieWer
Utility to simplify some routine processes: 
### Usage:

    lw [-c][--node][-r][--config] {component}
    
    	-c {argv}
            Count lines to print (default=1000)
        --node
            Choose node (default=0)
    	--config
            Show config file for choosen component
    	-r
            Restart component
    	--analize
            Statistic of error's count
    	--count-used
            Get number of uses
    	--help or -h
            This help
ex: restart nginx (if configured) : 

    lw -r ng
  
  
> Before installing configure ./lw_configs/vw.py

### Configuration:  
 - Set cfg_dir - directory where lw store configs
 - Set `user` to jump between servers
 - Edit masks: `mask`, `mask_restart` and `mask_config` - 4 args (`%s`) for `mask` and 2 args each for `mask_restart` and `mask_config`
 - `Freq_list_err` and `freq_list_warn` - most common errors and warn in logs to show into `analize` function
 - `Component`, `server`, `log_file_name`, `shortnames` - servers and shortnames must be with comma, if specified 1 value
 - String `components_t` must be after each `component` section

### Installation:

    python3 setup.py install (required root)

### Bugs

 - `%s` required only N times it defined in example (except `mask`, it can store both 3 and 4 args)
 - Additional args unavailable (ex: `-f` key for tail)
 - 1 method for restarting
