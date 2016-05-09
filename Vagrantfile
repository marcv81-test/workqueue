VAGRANTFILE_VERSION = "2"

require 'yaml'

env_filename = 'environments/vagrant.yml'

# Tentatively load environment
begin
  environment = YAML.load_file(env_filename)
rescue Exception => e
  STDERR.puts 'Error: ' + e.message
  exit(-1)
end

# Define hosts
Vagrant.configure(VAGRANTFILE_VERSION) do |config|
  environment['hosts'].each do |name, properties|
    config.vm.define name do |host|
      host.vm.box = properties['box']
      host.vm.hostname = name
      host.vm.network 'private_network', ip: properties['ip']
      host.vm.provider 'virtualbox' do |virtualbox|
        virtualbox.name = name
        virtualbox.memory = properties['memory']
      end
    end
  end
end
