import win32com.client

wmi=win32com.client.GetObject('winmgmts:') 
for p in wmi.InstancesOf('win32_process'):
    print(p.Name, p.Properties_('ProcessId'), int(p.Properties_('UserModeTime').Value)+int(p.Properties_('KernelModeTime').Value))
