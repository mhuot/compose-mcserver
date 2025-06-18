# Compose MCServer

A configurable Minecraft server deployment optimized for Oracle Cloud Infrastructure's generous **Always Free** ARM tier. This project leverages Docker Compose with automated infrastructure provisioning to run high-performance Minecraft servers at zero cost.

## Built on itzg/minecraft-server

This project is built upon the excellent [itzg/minecraft-server](https://github.com/itzg/docker-minecraft-server) Docker image by [@itzg](https://github.com/itzg). The itzg/minecraft-server project provides:

- **Comprehensive Minecraft server support** (Vanilla, Fabric, Forge, Quilt, and more)
- **Automatic server management** (updates, mod installation, configuration)
- **Extensive customization options** (plugins, datapacks, resource packs)
- **Production-ready stability** with millions of downloads

**Full credit to [@itzg](https://github.com/itzg) and contributors** for creating and maintaining the foundational Docker image that makes this deployment possible. Please star and support the [original project](https://github.com/itzg/docker-minecraft-server).

## Why Oracle Cloud Free Tier?

Oracle Cloud Infrastructure offers an unmatched **Always Free** tier perfect for Minecraft servers:

- **4 ARM CPU cores** (Ampere A1 - excellent performance)
- **24GB RAM** (more than most paid VPS options)
- **200GB boot storage** + additional block storage
- **10TB monthly egress** (outbound traffic)
- **No time limits** - truly free forever
- **Superior price/performance** compared to other cloud providers

## Features

- **Zero Cost Hosting**: Optimized for OCI's Always Free ARM tier
- **High Performance**: 4 ARM cores + 24GB RAM outperforms most paid alternatives  
- **Configurable**: All settings managed through YAML configuration
- **itzg/minecraft-server**: Built on the industry-standard Docker image
- **Infrastructure as Code**: Automated OCI provisioning with Terraform
- **Multiple Deployment Options**: Terraform automation or manual setup
- **Flexible Networking**: Public IP or custom domain configuration
- **Comprehensive Server Support**: Vanilla, Fabric, Forge, Quilt, and more via itzg image

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install pyyaml jinja2
   ```

2. **Configure Your Server**
   ```bash
   cp config.yaml.example config.yaml
   cp .env.example .env
   # Edit config.yaml and .env with your settings
   ```

3. **Generate Configuration Files**
   ```bash
   ./configure.py
   ```

4. **Start Your Server**
   ```bash
   docker compose up -d
   ```

## Configuration

### Basic Configuration

Edit `config.yaml` to customize your server:

```yaml
minecraft:
  server_name: "my-server"
  motd: "Welcome to My Server"
  difficulty: "normal"
  memory: "4G"
  ops: "admin,player2"
  port: 25565
  
  # Optional features
  enable_packwiz: false
  enable_vanillatweaks: false
```

### Environment Variables

Copy `.env.example` to `.env` and set sensitive values:

```bash
OCI_TENANCY_OCID=your_ocid_here
OCI_USER_OCID=your_user_ocid_here
```

## Optional Components

### VanillaTweaks Integration

Enable VanillaTweaks by setting in `config.yaml`:

```yaml
minecraft:
  enable_vanillatweaks: true
  vanillatweaks_files:
    - "vt-datapacks.json"
    - "vt-crafting.json"
```

Then place your VanillaTweaks JSON files in the project root.

### Packwiz Integration

Enable Packwiz by setting in `config.yaml`:

```yaml
minecraft:
  enable_packwiz: true
  packwiz_url: "https://your-server.com/pack.toml"
```

### Infrastructure Provisioning (Terraform)

Enable Terraform support in `config.yaml`:

```yaml
terraform:
  enabled: true
  oci:
    tenancy_ocid: "your-ocid"
    user_ocid: "your-user-ocid"
    # ... other settings
```

Then run:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

#### Using Oracle Cloud Infrastructure (OCI) Always Free ARM Server

This project is specifically designed to maximize OCI's **Always Free** ARM tier - the most generous free cloud offering available for Minecraft hosting:

**Free Tier Specs:**
- **4 OCPU ARM cores** (Ampere A1)
- **24GB RAM** 
- **200GB boot volume**
- **10TB monthly egress** (outbound traffic)
- **Always Free** (no time limits)

**Setup Instructions:**

1. **Create OCI Account**
   - Sign up at [oracle.com/cloud/free](https://oracle.com/cloud/free)
   - Complete identity verification (required for ARM instances)

2. **Generate API Keys**
   ```bash
   # Generate private key
   openssl genrsa -out ~/.ssh/oci.pem 2048
   
   # Generate public key
   openssl rsa -pubout -in ~/.ssh/oci.pem -out ~/.ssh/oci_public.pem
   
   # Get fingerprint
   openssl rsa -pubout -outform DER -in ~/.ssh/oci.pem | openssl md5 -c
   ```

3. **Configure OCI User**
   - Go to **User Settings** → **API Keys** → **Add API Key**
   - Upload your public key (`oci_public.pem`)
   - Note the fingerprint and user OCID

4. **Update Configuration**
   
   Edit `config.yaml`:
   ```yaml
   terraform:
     enabled: true
     oci:
       tenancy_ocid: "ocid1.tenancy.oc1..your-tenancy-ocid"
       user_ocid: "ocid1.user.oc1..your-user-ocid"
       private_key_path: "~/.ssh/oci.pem"
       fingerprint: "aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99"
       region: "us-chicago-1"  # or your preferred region
   ```

5. **Deploy Infrastructure**
   ```bash
   ./configure.py
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

**ARM + itzg Optimization:**
- **ARM64-optimized** Ubuntu 22.04 image for maximum efficiency
- **Full resource allocation**: All 4 OCPUs and 24GB RAM dedicated to Minecraft
- **itzg/minecraft-server**: Proven Docker image with ARM support
- **Aikar JVM flags**: Memory-optimized for ARM architecture
- **Automatic firewall**: Preconfigured for Minecraft and RCON ports

**Always Free Benefits:**
- **$0/month forever**: No hidden costs or time limits
- **10TB monthly egress**: Supports 100+ concurrent players easily
- **200GB boot storage**: Room for worlds, mods, and backups
- **Better than paid alternatives**: Outperforms most $20-40/month VPS options

#### Manual Setup (Alternative to Terraform/Ansible)

If you prefer to set up your OCI instance manually:

**1. Create ARM Instance Manually**
- Go to **Compute** → **Instances** → **Create Instance**
- **Name**: `minecraft-server`
- **Compartment**: Select your compartment
- **Availability Domain**: Any AD with ARM availability
- **Image**: Ubuntu 22.04 (ARM64)
- **Shape**: VM.Standard.A1.Flex
- **OCPUs**: 4, **Memory**: 24GB
- **Networking**: Create/use VCN with public subnet
- **SSH Keys**: Add your public key
- **Boot Volume**: 200GB (included in free tier)

**2. Configure Firewall Rules**
```bash
# Connect to your instance
ssh ubuntu@your-instance-ip

# Configure iptables for Minecraft
sudo iptables -A INPUT -p tcp --dport 25565 -j ACCEPT  # Minecraft
sudo iptables -A INPUT -p tcp --dport 25575 -j ACCEPT  # RCON (optional)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT     # SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT     # HTTP (optional)
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT    # HTTPS (optional)

# Save rules
sudo netfilter-persistent save
```

**3. Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Install Python dependencies
sudo apt install python3-pip -y
pip3 install pyyaml jinja2

# Install Git
sudo apt install git -y
```

**4. Deploy Minecraft Server**
```bash
# Clone repository
git clone https://github.com/mhuot/compose-mcserver.git
cd compose-mcserver

# Configure server
cp config.yaml.example config.yaml
cp .env.example .env

# Edit configuration files
nano config.yaml  # Set your server preferences
nano .env         # Add any secrets if needed

# Generate configuration
python3 configure.py

# Start server
docker compose up -d

# Check status
docker compose ps
docker compose logs -f
```

**5. OCI Network Security Rules**
- Go to **Networking** → **Virtual Cloud Networks** → Your VCN → **Security Lists**
- Add **Ingress Rules**:
  - **Source CIDR**: `0.0.0.0/0`
  - **Protocol**: TCP
  - **Destination Port**: `25565` (Minecraft)
  - **Destination Port**: `25575` (RCON, optional)

**6. Connect to Your Server**
- Find your public IP in the OCI console
- Connect using: `your-public-ip:25565`

## Security Best Practices

Running a public Minecraft server requires attention to security. Follow these recommendations:

### Use Non-Standard Ports

**Highly Recommended**: Change from the default port 25565 to reduce automated attacks and port scans.

**Configure Custom Port:**

Edit `config.yaml`:
```yaml
minecraft:
  port: 25567  # Use any port 1024-65535 (avoid 25565)
  rcon_port: 25577  # Also change RCON port
```

**Update Firewall Rules:**
```bash
# Remove default port access
sudo iptables -D INPUT -p tcp --dport 25565 -j ACCEPT
sudo iptables -D INPUT -p tcp --dport 25575 -j ACCEPT

# Add your custom ports
sudo iptables -A INPUT -p tcp --dport 25567 -j ACCEPT  # Your custom Minecraft port
sudo iptables -A INPUT -p tcp --dport 25577 -j ACCEPT  # Your custom RCON port

# Save changes
sudo netfilter-persistent save
```

**Update OCI Security Lists:**
- Remove rules for ports 25565/25575
- Add rules for your custom ports (25567/25577)

### Additional Security Measures

**1. Enable Online Mode (Authentication)**
```yaml
minecraft:
  online_mode: true  # Requires legitimate Minecraft accounts
```

**2. Whitelist Players (Recommended)**
```yaml
minecraft:
  whitelist: "player1,player2,player3"
  enforce_whitelist: true
```

**3. Disable RCON for Public Servers**
```yaml
minecraft:
  enable_rcon: false  # Disable remote console access
```

**4. Configure Rate Limiting**
```yaml
minecraft:
  max_players: 20  # Limit concurrent connections
  max_world_size: 29999984  # Prevent world border exploitation
```

**5. Regular Backups**
```bash
# Set up automated backups (run via cron)
docker exec mc-server rcon-cli save-all
docker exec mc-server rcon-cli save-off
tar -czf backup-$(date +%Y%m%d).tar.gz ./data/
docker exec mc-server rcon-cli save-on
```

**6. Monitor Server Logs**
```bash
# Watch for suspicious activity
docker compose logs -f | grep -E "(banned|kicked|timeout)"
```

**7. Keep Software Updated**
```bash
# Regular updates
docker compose pull  # Update itzg/minecraft-server image
docker compose up -d  # Restart with latest image
```

**8. Fail2Ban Protection (Advanced)**
```bash
# Install fail2ban
sudo apt install fail2ban

# Create Minecraft jail configuration
sudo nano /etc/fail2ban/jail.d/minecraft.conf
```

Add to minecraft.conf:
```ini
[minecraft]
enabled = true
port = 25567  # Your custom port
protocol = tcp
filter = minecraft
logpath = /path/to/minecraft/logs/latest.log
maxretry = 3
bantime = 3600
findtime = 600
```

### Security Checklist

- [ ] **Changed default ports** (25565 → custom port)
- [ ] **Enabled online mode** (prevents cracked clients)
- [ ] **Configured whitelist** (known players only)
- [ ] **Disabled RCON** (unless specifically needed)
- [ ] **Set player limits** (prevent resource exhaustion)
- [ ] **Regular backups** (automated daily/weekly)
- [ ] **Monitor logs** (watch for attacks/issues)
- [ ] **Updated software** (latest itzg image + OCI patches)
- [ ] **Firewall configured** (custom ports only)
- [ ] **Strong server passwords** (if using RCON/admin tools)

### Server Automation (Ansible)

Enable Ansible support in `config.yaml`:

```yaml
ansible:
  enabled: true
  hosts:
    mcserver1:
      ansible_host: "your-server-ip"
      ansible_user: "ubuntu"
```

Then run:
```bash
ansible-playbook -i ansible/inventory ansible/mcserver.yml
```

## Network Access

### Using Public IP

The simplest way to connect to your server is using the public IP address:

1. **Find your server's public IP** (from your cloud provider or `curl ifconfig.me`)
2. **Share the IP with players**: `your.server.ip:25565`
3. **Configure firewall** to allow port 25565 (and 25575 for RCON if needed)

### Using a Custom Domain

If you want to use a domain like `minecraft.example.com`:

1. **Purchase a domain** from any registrar (Namecheap, GoDaddy, etc.)
2. **Create an A record** pointing to your server's public IP:
   ```
   Type: A
   Name: minecraft (or @ for root domain)
   Value: your.server.ip.address
   TTL: 300 (or your registrar's default)
   ```
3. **Wait for DNS propagation** (usually 5-60 minutes)
4. **Players connect using**: `minecraft.example.com:25565`

### SRV Records (Optional)

To remove the port number from the connection string:

1. **Create an SRV record**:
   ```
   Type: SRV
   Name: _minecraft._tcp
   Priority: 0
   Weight: 5
   Port: 25565
   Target: minecraft.example.com
   ```
2. **Players can now connect with just**: `example.com`

### Port Forwarding (Self-Hosted)

If running from home:

1. **Configure router port forwarding**:
   - External port: 25565
   - Internal port: 25565
   - Protocol: TCP
   - Target: Your server's local IP
2. **Use your public IP** or dynamic DNS service

## Configuration Script

The `configure.py` script generates all configuration files from templates:

```bash
# Generate all files
./configure.py

# Use custom config file
./configure.py --config my-config.yaml

# Backup existing files before generating
./configure.py --backup
```

## File Structure

```
compose-mcserver/
├── configure.py              # Configuration generator
├── config.yaml.example      # Example configuration
├── .env.example             # Example environment variables
├── docker-compose.yml       # Generated Docker Compose file
├── templates/               # Jinja2 templates
│   ├── docker-compose.yml.j2
│   ├── terraform/
│   └── ansible/
├── terraform/               # Generated Terraform files
├── ansible/                 # Generated Ansible files
├── data/                    # Minecraft server data
├── vt-*.json               # VanillaTweaks configuration (optional)
└── LICENSE                  # Apache 2.0 License
```

## Troubleshooting

### Permission Issues
```bash
chmod +x configure.py
```

### Docker Issues
Make sure Docker and Docker Compose are installed and running.

### Missing Dependencies
```bash
pip install -r requirements.txt  # If available
# or manually:
pip install pyyaml jinja2
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the configuration generation
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue for bugs or feature requests
- Check the configuration examples in `config.yaml.example`
- Review the generated files for debugging