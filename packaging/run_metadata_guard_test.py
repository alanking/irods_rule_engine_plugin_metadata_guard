import subprocess

if __name__ == "__main__":
    subprocess.call(['sudo', 'python', '-m', 'xmlrunner', 'irods.test.test_rule_engine_plugin_metadata_guard'])

