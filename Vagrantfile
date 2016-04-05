VAGRANTFILE_VERSION = "2"

require 'yaml'

# Tentatively load environment
begin
  if !ENV.has_key?('ENVIRONMENT')
    raise Exception, "ENVIRONMENT is undefined"
  end
  environment = YAML.load_file(ENV['ENVIRONMENT'])
rescue Exception => e
  STDERR.puts 'Error: ' + e.message
  STDERR.puts 'ENVIRONMENT must point to a valid environment definition file'
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
