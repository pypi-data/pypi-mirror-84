# Netbox Work Logs Plugin

This the netbox Device/Virtual Machine work logs plugin.
You can use [netbox_work_logs](https://github.com/vas-git/netbox-work-logs) plugin in Github.com

## Installing Netbox Work Logs Plugin
The instructions below detail the process for installing and enabling a Netbox work logs plugin.

### Install Package
Download and install the plugin package per its installation instructions. Plugins published via PyPI are typically installed using pip. Be sure to install the plugin within Netbox`s virtual environment.

please refer [how to use netbox plugins](https://netbox.readthedocs.io/en/stable/plugins/)


```
$ source /opt/netbox/venv/bin/activate

(venv)$ pip install netbox_work_logs==[latest version]
```

### Enable the Plugin

In `configuration.py`, add the plugin`s name to the `PLUGIINS` list:

```
PLUGINS = [
    'netbox_work_logs',
]
```

### Configure Plugin
Open `configuration.py` with your preferred editor to begin configuring of Netbox work logs plugin. The following configuration are required only when you migrate the model of the netbox work logs plugin to the Netbox database.

```
DEVELOPER=True 
```

### Run Database Migrations

The Netbox work logs plugin has 3 models related with Virtual Machine / Device work logs, and work logs categories.
To introduce these new db models, run the provided schema migrations.
Next, we can apply the migration of the Netbox_work_logs model to the database with the `migrate` command

```
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py makemigrations netbox_work_logs
(venv) $ python3 manage.py migrate netbox_work_logs
```

### Restart service

Then, restart the `netbox` and `netbox-rq` services to enable them

```
# systemctl restart netbox netbox-rq
# systemctl restart nginx
```

## Reference

Please refer [Netbox plugin development document](https://netbox.readthedocs.io/en/stable/plugins/development/)