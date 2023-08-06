# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2019 Benjamin Marandel - All Rights Reserved.
################################################################################

"""
This module defines the class ESTPPolicyOnAccessScan.
"""

import xml.etree.ElementTree as et
from ...policies import Policy

class ESTPPolicyOnAccessScan(Policy):
    """
    The ESTPPolicyOnAccessScan class can be used to edit the Endpoint Security
    Threat Prevention policy: On-Access Scan.
    """

    def __init__(self, policy_from_estppolicies=None):
        super(ESTPPolicyOnAccessScan, self).__init__(policy_from_estppolicies)
        #super(ESTPPolicyOnAccessScan, self).__init__(policy_from_estppolicies)
        if policy_from_estppolicies is not None:
            if self.get_type() != 'EAM_General_Policies':
                raise ValueError('Wrong policy! Policy type must be "EAM_General_Policies".')

    def __repr__(self):
        return 'ESTPPolicyOnAccessScan()'

    # ------------------------------ On-Access Policy ------------------------------
    # On-Access Scan:
    #   Enable On-Access Scan
    def get_on_access_scan(self):
        """
        Get the On-Access Scan feature state
        """
        return self.get_setting_value('General', 'bOASEnabled')

    def set_on_access_scan(self, mode):
        """
        Set the On-Access Scan feature state
        """
        return self.set_setting_value('General', 'bOASEnabled', mode)

    on_access_scan = property(get_on_access_scan, set_on_access_scan)

    #	Enable On-Access Scan on system startup
    def get_scan_on_startup(self):
        """
        Get the On-Access Scan on system startup state
        """
        return self.get_setting_value('General', 'bStartEnabled')

    def set_scan_on_startup(self, mode):
        """
        Set the On-Access Scan on system startup state
        """
        return self.set_setting_value('General', 'bStartEnabled', mode)

    scan_on_startup = property(get_scan_on_startup, set_scan_on_startup)

	#	Allow users to disable On-Access Scan from the McAfee system tray icon
    def get_allow_user_to_disable_oas(self):
        """
        Get state of Allow users to disable On-Access Scan from the McAfee system tray icon
        """
        return self.get_setting_value('General', 'bAllowDisableViaMcTray')

    def set_allow_user_to_disable_oas(self, mode):
        """
        Set state of Allow users to disable On-Access Scan from the McAfee system tray icon
        """
        return self.set_setting_value('General', 'bAllowDisableViaMcTray', mode)

    allow_user_to_disable_oas = property(get_allow_user_to_disable_oas,
                                         set_allow_user_to_disable_oas)

    #	Specify maximum number of seconds for each file scan
    def get_max_scan_time_enforced(self):
        """
        Get if maximum scan time is enforced
        """
        return self.get_setting_value('General', 'bEnforceMaxScanTime')

    def set_max_scan_time_enforced(self, mode):
        """
        Set enforcement of maximum scan time
        """
        return self.set_setting_value('General', 'bEnforceMaxScanTime', mode)

    max_scan_time_enforced = property(get_max_scan_time_enforced, set_max_scan_time_enforced)

    def get_max_scan_time(self):
        """
        Get the maximum number of seconds for each file scan
        """
        return int(self.get_setting_value('General', 'dwScannerThreadTimeout'))

    def set_max_scan_time(self, int_seconds):
        """
        Set the maximum number of seconds for each file scan
        """
        if int_seconds < 10:
            raise ValueError('Timeout below 10 seconds is not accepted.')
        return self.set_setting_value('General', 'dwScannerThreadTimeout', int_seconds)

    max_scan_time = property(get_max_scan_time, set_max_scan_time)

    #	Scan boot sectors
    def get_scan_boot_sectors(self):
        """
        Get state of Scan boot sectors
        """
        return self.get_setting_value('General', 'bScanBootSectors')

    def set_scan_boot_sectors(self, mode):
        """
        Set state of Scan boot sectors
        """
        return self.set_setting_value('General', 'bScanBootSectors', mode)

    scan_boot_sectors = property(get_scan_boot_sectors, set_scan_boot_sectors)

    #	Scan processes on service startup and content update
    def get_scan_process_startup(self):
        """
        Get state of Scan processes on service startup and content update
        """
        return self.get_setting_value('General', 'scanProcessesOnEnable')

    def set_scan_process_startup(self, mode):
        """
        Set state of Scan processes on service startup and content update
        """
        return self.set_setting_value('General', 'scanProcessesOnEnable', mode)

    scan_process_startup = property(get_scan_process_startup, set_scan_process_startup)

    #	Scan trusted installers
    def get_scan_trusted_installers(self):
        """
        Get state of Scan trusted installers
        """
        return self.get_setting_value('General', 'scanTrustedInstallers')

    def set_scan_trusted_installers(self, mode):
        """
        Set state of Scan trusted installers
        """
        return self.set_setting_value('General', 'scanTrustedInstallers', mode)

    scan_trusted_installers = property(get_scan_trusted_installers, set_scan_trusted_installers)

    #	Scan when copying between local folders
    def get_scan_copy_between_local_folders(self):
        """
        Get state of Scan when copying between local folders
        """
        return self.get_setting_value('General', 'scanCopyLocalFolders')

    def set_scan_copy_between_local_folders(self, mode):
        """
        Set state of Scan when copying between local folders
        """
        return self.set_setting_value('General', 'scanCopyLocalFolders', mode)

    scan_copy_between_local_folders = property(get_scan_copy_between_local_folders,
                                               set_scan_copy_between_local_folders)

    #	Scan when copying from network folders and removable drives
    def get_scan_copy_from_network(self):
        """
        Get state of Scan when copying from network folders and removable drives
        """
        return self.get_setting_value('General', 'scanCopyNetworkRemovable')

    def set_scan_copy_from_network(self, mode):
        """
        Set state of Scan when copying from network folders and removable drives
        """
        return self.set_setting_value('General', 'scanCopyNetworkRemovable', mode)

    scan_copy_from_network = property(get_scan_copy_from_network, set_scan_copy_from_network)

    #	Detect suspicious email attachments
    def get_scan_email_attachments(self):
        """
        Get state of Detect suspicious email attachments
        """
        return self.get_setting_value('General', 'scanEmailAttachments')

    def set_scan_email_attachments(self, mode):
        """
        Set state of Detect suspicious email attachments
        """
        return self.set_setting_value('General', 'scanEmailAttachments', mode)

    scan_email_attachments = property(get_scan_email_attachments, set_scan_email_attachments)

    #	Disable read/write scan of Shadow Copy volumes for SYSTEM process (improves performance)
    def get_scan_shadow_copy(self):
        """
        Get state of Read/Write scan of Shadow Copy volumes for SYSTEM process
        """
        mode = self.get_setting_value('General', 'scanShadowCopyDisableStatus')
        return '0' if mode == '1' else '1'

    def set_scan_shadow_copy(self, mode):
        """
        Set state of Read/Write scan of Shadow Copy volumes for SYSTEM process
        """
        mode = '0' if mode == '1' else '1'
        return self.set_setting_value('General', 'scanShadowCopyDisableStatus', mode)

    scan_shadow_copy = property(get_scan_shadow_copy, set_scan_shadow_copy)

    # ------------------------------ On-Access Policy ------------------------------
    # McAfee GTI:
    #	Enable McAfee GTI
    #   0 = OFF         Gti().DISABLED
    #   1 = Very Low    Gti().VERY_LOW
    #   2 = Low         Gti().LOW
    #   3 = Medium      Gti().MEDIUM
    #   4 = High        Gti().HIGH
    #   5 = Very High   Gti().VERY_HIGH
    def get_gti_level(self):
        """
        Get the GTI level (Use Gti class from constants)
        """
        return self.get_setting_value('GTI', 'GTISensitivityLevel')

    def set_gti_level(self, level):
        """
        Set the GTI level (Use Gti class from constants)
        """
        if level not in ['0', '1', '2', '3', '4', '5']:
            raise ValueError('GTI sensitivity level must be within ["0", "1", "2", "3", "4", "5"].')
        return self.set_setting_value('GTI', 'GTISensitivityLevel', level)

    gti_level = property(get_gti_level, set_gti_level)

    # ------------------------------ On-Access Policy ------------------------------
    # Antimalware Scan Interface:
    #	Enable AMSI (provides enhanced script scanning)
    def get_scan_amsi(self):
        """
        Get state of Enable AMSI (provides enhanced script scanning)
        """
        return self.get_setting_value('General', 'scanUsingAMSIHooks')

    def set_scan_amsi(self, mode):
        """
        Set state of Enable AMSI (provides enhanced script scanning)
        """
        return self.set_setting_value('General', 'scanUsingAMSIHooks', mode)

    scan_amsi = property(get_scan_amsi, set_scan_amsi)

    #	Enable Observe mode (Events are generated but actions are not enforced)
    def get_scan_amsi_observe_mode(self):
        """
        Get state of Enable AMSI Observe mode (Events are generated but actions are not enforced)
        """
        return self.get_setting_value('General', 'enableAMSIObserveMode')

    def set_scan_amsi_observe_mode(self, mode):
        """
        Set state of Enable AMSI Observe mode (Events are generated but actions are not enforced)
        """
        return self.set_setting_value('General', 'enableAMSIObserveMode', mode)

    scan_amsi_observe_mode = property(get_scan_amsi_observe_mode, set_scan_amsi_observe_mode)

    # ------------------------------ On-Access Policy ------------------------------
    # Threat Detection User Messaging:
    #	Display the On-Access Scan window to users when a threat is detected
    def get_show_alert(self):
        """
        Get state of Display the On-Access Scan window to users when a threat is detected
        """
        return self.get_setting_value('Alerting', 'bShowAlerts')

    def set_show_alert(self, mode):
        """
        Set state of Display the On-Access Scan window to users when a threat is detected
        """
        return self.set_setting_value('Alerting', 'bShowAlerts', mode)

    show_alert = property(get_show_alert, set_show_alert)

    #	Message: (Default = McAfee Endpoint Security detected a threat.)
    def get_alert_message(self):
        """
        Get Threat Detection message
        """
        return self.get_setting_value('Alerting', 'szDialogMessage')

    def set_alert_message(self, str_message="McAfee Endpoint Security detected a threat."):
        """
        Set Threat Detection message (256 caracters maximum)
        """
        if len(str_message) == 0 or len(str_message) > 256:
            raise ValueError('The message cannot be empty or longer than 256 caracters.')
        return self.set_setting_value('Alerting', 'szDialogMessage', str_message)

    alert_message = property(get_alert_message, set_alert_message)

    # ------------------------------ On-Access Policy ------------------------------
    # Process Settings:
    def get_use_standard_settings_only(self):
        """
        Get Use Standard settings for all processes or
        Configure different settings for High Risk and Low Risk processes
        """
        return self.get_setting_value('General', 'bOnlyUseDefaultConfig')

    def set_use_standard_settings_only(self, mode):
        """
        Set Use Standard settings for all processes or
        Configure different settings for High Risk and Low Risk processes
        """
        return self.set_setting_value('General', 'bOnlyUseDefaultConfig', mode)

    use_standard_settings_only = property(get_use_standard_settings_only,
                                          set_use_standard_settings_only)

    # ------------------------------ On-Access Policy ------------------------------
    # Process Settings:
    def get_process_list(self):
        """
        Get the process list
        (Standard settings will apply to all unlisted processes.)
        Return a ProcessList object.
        """
        table = None
        section_obj = self.root.find('./EPOPolicySettings/Section[@name="Application"]')
        if section_obj is not None:
            setting_obj = section_obj.find('Setting[@name="dwApplicationCount"]')
            max_rows = int(setting_obj.get('value'))
            table = list()
            for row in range(max_rows):
                row_value = list()
                setting_obj = section_obj.find('Setting[@name="szApplicationItem_{}"]'.format(row))
                row_value.append(setting_obj.get('value'))
                setting_obj = section_obj.find('Setting[@name="TypeItem_{}"]'.format(row))
                if setting_obj.get('value') == '0':
                    row_value.append('Low Risk')
                else:
                    row_value.append('High Risk')
                table.append(row_value)
        return table

    def set_process_list(self, table):
        """
        Set the process list with a ProcessList object as input
        Return true or false.
        """
        success = False
        section_obj = self.root.find('./EPOPolicySettings/Section[@name="Application"]')
        if section_obj is not None:
            success = True
            parent_obj = self.root.find('./EPOPolicySettings')
            parent_obj.remove(section_obj)
            section_obj = et.SubElement(parent_obj, 'Section', name='Application')
            if len(table) > 0:
                et.SubElement(section_obj, 'Setting',
                              {"name":'dwApplicationCount', "value":str(len(table))})
                for index, row in enumerate(table):
                    et.SubElement(section_obj, 'Setting',
                                  {"name":'szApplicationItem_{}'.format(index), "value":row[0]})
                    if row[1] == 'Low Risk':
                        et.SubElement(section_obj, 'Setting',
                                      {"name":'TypeItem_x{}'.format(index), "value":'0'})
                    elif row[1] == 'High Risk':
                        et.SubElement(section_obj, 'Setting',
                                      {"name":'TypeItem_x{}'.format(index), "value":'1'})
                    else:
                        raise ValueError('Risk level unknown: {}.'.format(row[1]))
        return success

    process_list = property(get_process_list, set_process_list)

    # ---------------------- On-Access Policy - Standard ---------------------------
    # Process Settings:
    #	Process Type: Standard
    def get_when_to_scan(self):
        """
        Get When to scan, Reading/Writing.
        Returns a int value as following
        '0':When writing to disk
        '1':When reading from disk
        '2':Let McAfee decide
        """
        writing_mode = self.get_setting_value('Default-Detection', 'bScanWriting')
        reading_mode = self.get_setting_value('Default-Detection', 'bScanReading')
        if writing_mode == '1' and reading_mode == '1':
            level = '2'
        elif reading_mode == '1':
            level = '1'
        else:
            level = '0'
        return level

    def set_when_to_scan(self, level):
        """
        Set When to scan, Reading/Writing.
        Use following level as input:
        '0':When writing to disk
        '1':When reading from disk
        '2':Let McAfee decide
        """
        success = False
        if level not in ['0', '1', '2']:
            raise ValueError('Level must be within ["0", "1", "2"].')
        success = True
        if level == '0':
            writing_mode = '1'
            reading_mode = '0'
        elif level == '1':
            writing_mode = '0'
            reading_mode = '1'
        else:
            writing_mode = '1'
            reading_mode = '1'
        self.set_setting_value('Default-Detection', 'bScanWriting', writing_mode)
        self.set_setting_value('Default-Detection', 'bScanReading', reading_mode)
        return success

    when_to_scan = property(get_when_to_scan, set_when_to_scan)

    #	Scanning - What to Scan
    def get_what_to_scan(self):
        """
        Get what to scan
        Returns level and extension as a tupple:
        '1': All files
        '2': Default and specified file types
        '3': Default and specified file types with scan for macros
        '4': Specified file types only (Extension must be defined)
             -> To scan also all files with no extension add the extension ':::'.
        """
        level = self.get_setting_value('Default-Detection', 'extensionMode')
        extensions = self.get_setting_value('Default-Detection', 'szProgExts')
        return (level, extensions)

    def set_what_to_scan(self, level, extensions=''):
        """
        Set what to scan
        Use level and extension as inputs:
        '1': All files
        '2': Default and specified file types
        '3': Default and specified file types with scan for macros
        '4': Specified file types only (Extension must be defined)
             -> To scan also all files with no extension add the extension ':::'.
        """
        if level not in ['1', '2', '3', '4']:
            raise ValueError('Level must be within ["1", "2", "3", "4"].')
        if level == '4' and len(extensions) < 3:
            raise ValueError('Extensions list, comma separated, must be defined for this level.')
        self.set_setting_value('Default-Detection', 'extensionMode', level)
        self.set_setting_value('Default-Detection', 'szProgExts', extensions)
        return True

    what_to_scan = property(get_what_to_scan, set_what_to_scan)

    #	Scanning - What to Scan
    def get_scan_network_drives(self):
        """
        Get On network drives
        """
        return self.get_setting_value('Default-Detection', 'bNetworkScanEnabled')

    def set_scan_network_drives(self, mode):
        """
        Set On network drives
        """
        return self.set_setting_value('Default-Detection', 'bNetworkScanEnabled', mode)

    scan_network_drives = property(get_scan_network_drives, set_scan_network_drives)

    #	Scanning - What to Scan
    def get_scan_backups(self):
        """
        Get Opened for backups
        """
        return self.get_setting_value('Default-Detection', 'bScanBackupReads')

    def set_scan_backups(self, mode):
        """
        Set Opened for backups
        """
        return self.set_setting_value('Default-Detection', 'bScanBackupReads', mode)

    scan_backups = property(get_scan_backups, set_scan_backups)

    #	Scanning - What to Scan
    def get_scan_archives(self):
        """
        Get Compressed archive files
        """
        return self.get_setting_value('Default-Detection', 'bScanArchives')

    def set_scan_archives(self, mode):
        """
        Set Compressed archive files
        """
        return self.set_setting_value('Default-Detection', 'bScanArchives', mode)

    scan_archives = property(get_scan_archives, set_scan_archives)

    #	Scanning - What to Scan
    def get_scan_mime(self):
        """
        Get Compressed MIME-encoded files
        """
        return self.get_setting_value('Default-Detection', 'bScanMime')

    def set_scan_mime(self, mode):
        """
        Set Compressed MIME-encoded files
        """
        return self.set_setting_value('Default-Detection', 'bScanMime', mode)

    scan_mime = property(get_scan_mime, set_scan_mime)

    #	Scanning - Additional scan options
    def get_scan_pup(self):
        """
        Get Detect unwanted programs
        """
        return self.get_setting_value('Default-Detection', 'bApplyNVP')

    def set_scan_pup(self, mode):
        """
        Set Detect unwanted programs
        """
        return self.set_setting_value('Default-Detection', 'bApplyNVP', mode)

    scan_pup = property(get_scan_pup, set_scan_pup)

    #	Scanning - Additional scan options
    def get_scan_unknown_threats(self):
        """
        Get Detect unknown program threats
        """
        return self.get_setting_value('Default-Detection', 'bUnknownProgramHeuristics')

    def set_scan_unknown_threats(self, mode):
        """
        Set Detect unknown program threats
        """
        return self.set_setting_value('Default-Detection', 'bUnknownProgramHeuristics', mode)

    scan_unknown_threats = property(get_scan_unknown_threats, set_scan_unknown_threats)

    #	Scanning - Additional scan options
    def get_scan_unknown_macro(self):
        """
        Get Detect unknown macro threats
        """
        return self.get_setting_value('Default-Detection', 'bUnknownMacroHeuristics')

    def set_scan_unknown_macro(self, mode):
        """
        Set Detect unknown macro threats
        """
        return self.set_setting_value('Default-Detection', 'bUnknownMacroHeuristics', mode)

    scan_unknown_macro = property(get_scan_unknown_macro, set_scan_unknown_macro)

    # ---------------------- On-Access Policy - Standard ---------------------------
    #	Actions:
    def get_action_threat_first_response(self):
        """
        Get Action - Threat detection first response
        Return the value of the current level
        '1': Clean files
        '2': Delete files
        '3': Deny access to files
        """
        return self.get_setting_value('Default-Detection', 'uAction')

    def set_action_threat_first_response(self, action):
        """
        Set Action - Threat detection first response
        Use the following value:
        '1': Clean files
        '2': Delete files
        '3': Deny access to files
        """
        if action not in ['1', '2', '3']:
            raise ValueError('Action must be within ["1", "2", "3"].')
        return self.set_setting_value('Default-Detection', 'uAction', action)

    action_threat_first_response = property(get_action_threat_first_response,
                                            set_action_threat_first_response)

    def get_action_threat_second_response(self):
        """
        Get Action - If first response fails:
        Secondary action must greater than the first one
        '2':Delete files
        '3':Deny access to files
        If first = '3' -> No secondary options available for this action.
        """
        return self.get_setting_value('Default-Detection', 'uSecAction')

    def set_action_threat_second_response(self, action):
        """
        Set Action - If first response fails:
        Secondary action must greater than the first one
        '2':Delete files
        '3':Deny access to files
        If first = '3' -> No secondary options available for this action.
        """
        if action not in ['2', '3']:
            raise ValueError('Action must be within ["2", "3"].')
        first_action = int(self.get_setting_value('Default-Detection', 'uAction'))
        if int(action) <= first_action:
            raise ValueError('Action must be greater than the first response.')
        return self.set_setting_value('Default-Detection', 'uSecAction', action)

    action_threat_second_response = property(get_action_threat_second_response,
                                             set_action_threat_second_response)

    def get_action_pup_first_response(self):
        """
        Get Action - Unwanted program first response:
        '1':Clean files
        '2':Delete files
        '3':Deny access to files
        '4':Allow access to files
        """
        return self.get_setting_value('Default-Detection', 'uAction_Program')

    def set_action_pup_first_response(self, action):
        """
        Set Action - Unwanted program first response:
        '1':Clean files
        '2':Delete files
        '3':Deny access to files
        '4':Allow access to files
        """
        if action not in ['1', '2', '3', '4']:
            raise ValueError('Action must be within ["1", "2", "3", "4"].')
        return self.set_setting_value('Default-Detection', 'uAction_Program', action)

    action_pup_first_response = property(get_action_pup_first_response,
                                         set_action_pup_first_response)

    def get_action_pup_second_response(self):
        """
        Get Action - If first response fails:
        '2':Delete files
        '3':Deny access to files
        '4':Allow access to files
        If first >= '3' -> No secondary options available for this action.
        """
        return self.get_setting_value('Default-Detection', 'uSecAction_Program')

    def set_action_pup_second_response(self, action):
        """
        Set Action - If first response fails:
        '2':Delete files
        '3':Deny access to files
        '4':Allow access to files
        If first >= '3' -> No secondary options available for this action.
        """
        if action not in ['2', '3', '4']:
            raise ValueError('Action must be within ["2", "3", "4"].')
        first_action = int(self.get_setting_value('Default-Detection', 'uAction_Program'))
        if int(action) <= first_action:
            raise ValueError('Action must be greater than the first response.')
        return self.set_setting_value('Default-Detection', 'uSecAction_Program', action)

    action_pup_second_response = property(get_action_pup_second_response,
                                          set_action_pup_second_response)

    # ---------------------- On-Access Policy - Standard ---------------------------
    #   Hidden setting
    def __get_action_on_error(self):
        """
        Get Hidden setting - Action on scanning error
        Default value set to: Allow access to files
        """
        return self.get_setting_value('Default-Detection', 'uScanErrorAction')


    def __get_action_on_timeout(self):
        """
        Get Hidden setting - Action on scanning time-out
        Default value set to: Allow access to files
        """
        return self.get_setting_value('Default-Detection', 'uTimeOutAction')

    # ---------------------- On-Access Policy - Standard ---------------------------
    #	Exclusions - Standard
    def get_exclusion_list(self, __section__='Default-Detection_Exclusions'):
        """
        Get exclusions list
        Return a list that can be used as ProcessList object.
        """
        table = None
        section_obj = self.root.find('./EPOPolicySettings/Section[@name="{}"]'.format(__section__))
        if section_obj is not None:
            setting_obj = section_obj.find('Setting[@name="dwExclusionCount"]')
            max_rows = int(setting_obj.get('value'))
            table = list()
            for row in range(max_rows):
                setting_obj = section_obj.find('Setting[@name="ExcludedItem_{}"]'.format(row))
                row_values = setting_obj.get('value').split('|')
                table.append(row_values)
        return table

    def set_exclusion_list(self, table, __section__='Default-Detection_Exclusions'):
        """
        Set exclusions list
        Use a list or a ProcessList object as input
        """
        success = False
        section_obj = self.root.find('./EPOPolicySettings/Section[@name="{}"]'.format(__section__))
        if section_obj is not None:
            success = True
            parent_obj = self.root.find('./EPOPolicySettings')
            parent_obj.remove(section_obj)
            section_obj = et.SubElement(parent_obj, 'Section', name=__section__)
            if len(table) > 0:
                et.SubElement(section_obj, 'Setting',
                              {"name":'dwExclusionCount', "value":str(len(table))})
                for index, row in enumerate(table):
                    exclusion = row[0] + '|' + row[1] + '|' + row[2] + '|' + row[3]
                    et.SubElement(section_obj, 'Setting',
                                  {"name":'ExcludedItem_{}'.format(index), "value":exclusion})
        return success

    exclusion_list = property(get_exclusion_list, set_exclusion_list)

    def get_overwrite_exclusions(self,  __section__='Default-Detection_Exclusions'):
        """
        Get Exclusions - Overwrite exclusions configured on the client
        """
        return self.get_setting_value(__section__, 'bOverwriteExclusions')

    def set_overwrite_exclusions(self, mode,  __section__='Default-Detection_Exclusions'):
        """
        Set Exclusions - Overwrite exclusions configured on the client
        """
        return self.set_setting_value(__section__, 'bOverwriteExclusions', mode)

    overwrite_exclusions = property(get_overwrite_exclusions, set_overwrite_exclusions)

    # ------------------------------ On-Access Policy ------------------------------
    # ScriptScan:
    def get_script_scan(self):
        """
        Get Enable ScriptScan
        """
        return self.get_setting_value('ScriptScan', 'scriptScanEnabled')

    def set_script_scan(self, mode):
        """
        Set Enable ScriptScan
        """
        return self.set_setting_value('ScriptScan', 'scriptScanEnabled', mode)

    script_scan = property(get_script_scan, set_script_scan)

    #	Exclude these URLs or partial URLs:
    def get_script_scan_exclusions(self):
        """
        Get Excluded URLs
        Return a list or an URLList object
        """
        excluded_urls = list()
        max_rows = int(self.get_setting_value('ScriptScanURLExclItems',
                                              'dwScriptScanURLExclItemCount'))
        for row in range(max_rows):
            excluded_urls.append(self.get_setting_value('ScriptScanURLExclItems',
                                                        'ScriptScanExclusionURL_{}'.format(row)))
        return excluded_urls

    def set_script_scan_exclusions(self, excluded_urls):
        """
        Set Excluded URLs
        Use URLList object as input
        """
        success = False
        section_obj = self.root.find('./EPOPolicySettings/Section[@name="ScriptScanURLExclItems"]')
        if section_obj is not None:
            success = True
            parent_obj = self.root.find('./EPOPolicySettings')
            parent_obj.remove(section_obj)
            section_obj = et.SubElement(parent_obj, 'Section', name='ScriptScanURLExclItems')
            et.SubElement(section_obj, 'Setting',
                          {"name":'dwScriptScanURLExclItemCount', "value":str(len(excluded_urls))})
            # Determine if there are some excluded urls
            if len(excluded_urls) > 0:
                for index, url in enumerate(excluded_urls):
                    et.SubElement(section_obj, 'Setting',
                                  {"name":'ScriptScanExclusionURL_{}'.format(index), "value":url})
        return success

    script_scan_exclusions = property(get_script_scan_exclusions, set_script_scan_exclusions)

class ProcessList:
    """
    The ProcessList class can be used to edit the list of process.
    All process names are associated to a risk level: Low or High.
    """

    def __init__(self, process_list = list()):
        self.proc_list = process_list

    def __repr__(self):
        return '<ProcessList which contains {} process(s)>'.format(len(self.proc_list))

    def __str__(self):
        txt = '| {0:40}| {1:13}|\n'.format('Process Name', 'Process Type')
        txt += '|:----------------------------------------|:-------------|'
        for row in self.proc_list:
            txt += '\n| {0:40}| {1:13}|'.format(row[0], row[1])
        return txt

    def add(self, process_name, process_type):
        """
        Add a process name of process type within the process list.
        :process_name: The name of the process.
        :process_type: 'Low Risk' or 'High Risk' value.
        """
        success = False
        if process_type not in ['Low Risk', 'High Risk']:
            raise ValueError('Process Type unknown. Value must be "Low Risk" or "High Risk".')
        if not self.contains(process_name):
            row = []
            row.append(process_name)
            row.append(process_type)
            self.proc_list.append(row)
            success = True
        return success

    def add_low_risk(self, process_name):
        """
        Add a low risk process name within the process list.
        :process_name: The name of the process.
        """
        return self.add(process_name, 'Low Risk')

    def add_high_risk(self, process_name):
        """
        Add a high risk process name within the process list.
        :process_name: The name of the process.
        """
        return self.add(process_name, 'High Risk')

    def remove(self, process_name):
        """
        Remove a process name of the process list.
        :process_name: The name of the process.
        """
        table = [row for row in self.proc_list if row[0] != process_name]
        self.proc_list = table
        return True

    def contains(self, process_name):
        """
        Return True if the process list contains a process name.
        :process_name: The name of the process.
        """
        search = [row[0] for row in self.proc_list if row[0] == process_name]
        return len(search) >= 1

    def contains_low_risk(self, process_name):
        """
        Return True if the process list contains a low risk process name.
        :process_name: The name of the process.
        """
        search = [row[0] for row in self.proc_list
                  if row[0] == process_name and row[1] == 'Low Risk']
        return len(search) >= 1

    def contains_high_risk(self, process_name):
        """
        Return True if the process list contains a high risk process name.
        :process_name: The name of the process.
        """
        search = [row[0] for row in self.proc_list
                  if row[0] == process_name and row[1] == 'High Risk']
        return len(search) >= 1

class ExclusionList:
    """
    The ExclusionList class can be used to edit the list of exclusion.
    What to exclude:
    '0': File age, changed with Minimum age in days
    '1': ? (not used or deprecated)
    '2': File age, created with Minimum age in days
    '3': File name or path (can include * or ? wildcards)
    '4': File type (can include the ? wildcard)

    When to excluded:
    1: On Write
    2: On Read
    4: Also exclude subfolders
    -> The final value is and addition of all options

    Name: File name or path, extension or days.

    Notes: Notes of the exclusion
    """

    def __init__(self, exclusion_list = list()):
        self.excl_list = exclusion_list

    def __repr__(self):
        return '<ExclusionList which contains {} exclusion(s)>'.format(len(self.excl_list))

    def __define_item__(self, action, value):
        item = ''
        if action == '0':
            item = 'Modified {} or more days ago'.format(value)
        elif action == '2':
            item = 'Created {} or more days ago'.format(value)
        elif action == '3':
            item = value
        elif action == '4':
            item = 'All files of type {}'.format(value)
        else:
            item = 'Unknown item'
        return item

    def __define_rights__(self, int_rights, action):
        rights = int_rights-4
        if rights >= 0:
            sub = True
        else:
            rights = rights+4
            sub = False
        rights = rights-2
        if rights >=0:
            read = True
        else:
            rights = rights+2
            read = False
        rights = rights-1
        write = bool(rights >= 0)

        if read and write:
            when = 'Read & Write'
        elif write:
            when = 'Write'
        else:
            when = 'Read'

        if action != '3':
            subfolder = '--'
        else:
            if sub:
                subfolder = 'Yes'
            else:
                subfolder = 'No'

        return (subfolder, when)

    def __compute_rights__(self, write, read, subfolder=False):
        rights = 0
        if write:
            rights = rights+1
        if read:
            rights = rights+2
        if subfolder:
            rights = rights+4
        return rights

    def __str__(self):
        txt = '| {0:70}| {1:12}| {2:13}| {3:30}|\n'.format(
              'Item:', 'Subfolders:', 'When:', 'Notes:')
        txt += '|:----------------------------------------------------------------------|'
        txt += ':------------|:-------------|:------------------------------|'
        for row in self.excl_list:
            item = self.__define_item__(row[0], row[2])
            rights = self.__define_rights__(int(row[1]), row[0])
            subfolder = rights[0]
            when = rights[1]
            notes = row[3]
            txt += '\n| {0:70}| {1:12}| {2:13}| {3:30}|'.format(item, subfolder, when, notes)
        return txt

    def __add_excl__(self, what, int_when, value, notes):
        if what not in ['0', '2', '3', '4']:
            raise ValueError('What to excluded value must be within ["0", "2", "3", "4"].')
        if int_when < 0 or int_when > 7:
            raise ValueError('When to excluded value must be within [0-7].')
        exclusion = []
        exclusion.append(what)
        exclusion.append(str(int_when))
        exclusion.append(value)
        exclusion.append(notes)
        self.excl_list.append(exclusion)
        return True

    def __contains_excl__(self, what, value):
        search = [row for row in self.excl_list if row[0] == what and row[2] == value]
        return len(search) >= 1

    def __remove__(self, what, value):
        table = [row for row in self.excl_list if not (row[0] == what and row[2] == value)]
        self.excl_list = table
        return True

    def add_folder(self, folder_path, on_write=True, on_read=True, with_subfolders=False, notes=''):
        """
        Add a folder exclusion
        """
        if folder_path[len(folder_path)-1] != '\\':
            raise ValueError('Path must be ended by "\\".')
        rights = self.__compute_rights__(on_write, on_read, with_subfolders)
        return self.__add_excl__('3', rights, folder_path, notes)

    def add_file_name(self, file_name_path, on_write=True, on_read=True, notes=''):
        """
        Add a file name exclusion
        """
        if file_name_path[len(file_name_path)-1] == '\\':
            raise ValueError('Path must not be ended by "\\".')
        rights = self.__compute_rights__(on_write, on_read)
        return self.__add_excl__('3', rights, file_name_path, notes)

    def add_file_type(self, file_extension, on_write=True, on_read=True, notes=''):
        """
        Add a file type exclusion
        """
        rights = self.__compute_rights__(on_write, on_read)
        return self.__add_excl__('4', rights, file_extension, notes)

    def add_file_modified(self, int_days=7, on_write=True, on_read=True, notes=''):
        """
        Add a file exclusion based on its last modified date
        """
        if int_days < 1:
            raise ValueError('Need one or more days.')
        rights = self.__compute_rights__(on_write, on_read)
        return self.__add_excl__('0', rights, str(int_days), notes)

    def add_file_created(self, int_days=7, on_write=True, on_read=True, notes=''):
        """
        Add a file exclusiopn based on its created date
        """
        if int_days < 1:
            raise ValueError('Need one or more days.')
        rights = self.__compute_rights__(on_write, on_read)
        return self.__add_excl__('2', rights, str(int_days), notes)

    def contains_folder(self, folder_path):
        """
        Returns True if a folder is excluded
        """
        return self.__contains_excl__('3', folder_path)

    def contains_file_name(self, file_name_path):
        """
        Returns True if a file name is excluded
        """
        return self.__contains_excl__('3', file_name_path)

    def contains_file_type(self, file_extension):
        """
        Returns True if a file extension is excluded
        """
        return self.__contains_excl__('4', file_extension)

    def contains_file_modified(self, int_days):
        """
        Returns True is a file is excluded based on its last modified date
        """
        return self.__contains_excl__('0', str(int_days))

    def contains_file_created(self, int_days):
        """
        Returns True is a file is excluded based on its created date
        """
        return self.__contains_excl__('2', str(int_days))

    def remove_folder(self, folder_path):
        """
        Remove a folder exclusion
        """
        return self.__remove__('3', folder_path)

    def remove_file_name(self, file_name_path):
        """
        Remove a file name exclusion
        """
        return self.__remove__('3', file_name_path)

    def remove_file_type(self, file_extension):
        """
        Remove a file extension exclusion
        """
        return self.__remove__('4', file_extension)

    def remove_file_modified(self, int_days):
        """
        Remove a file exclusion based on its last modified date
        """
        return self.__remove__('0', str(int_days))

    def remove_file_created(self, int_days):
        """
        Remove a file exclusion based on its created date
        """
        return self.__remove__('2', str(int_days))
