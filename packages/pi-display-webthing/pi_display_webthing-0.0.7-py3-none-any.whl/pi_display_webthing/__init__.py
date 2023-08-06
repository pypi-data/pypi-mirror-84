from string import Template
from pi_display_webthing.app import App
from pi_display_webthing.display_webthing import run_server



PACKAGENAME = 'pi_display_webthing'
ENTRY_POINT = "display"
DESCRIPTION = "A web connected LCD display module"



UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target network.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --hostname $hostname --verbose $verbose --port $port --name $name --address $address --expander $expander --num_lines $num_lines --num_chars $num_chars
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')




class DhtApp(App):

    def do_add_argument(self, parser):
        parser.add_argument('--expander', metavar='expander', required=False, type=str, help='the name of the port I²C port expander. Supported: PCF8574, MCP23008, MCP23017')
        parser.add_argument('--address', metavar='address', required=False, type=str, help='the I²C address of the LCD Module as hex string')
        parser.add_argument('--name', metavar='name', required=False, type=str, default="", help='the name of the display')
        parser.add_argument('--num_lines', metavar='num_lines', required=False, type=int, default=2, help='the number of lines')
        parser.add_argument('--num_chars', metavar='num_chars', required=False, type=int, default=16, help='the numberof chars per line')


    def do_additional_listen_example_params(self):
        return "--name NAS --expander PCF8574 --address 0x27 --num_lines 2 --num_chars 16"

    def do_process_command(self, command:str, hostname: str, port: int, verbose: bool, args) -> bool:
        if command == 'listen' and (args.expander is not None) and (args.address is not None):
            print("running " + self.packagename + " on " + hostname + ":" + str(port) + " (LCD " + str(args.num_lines)  + "/" + str(args.num_chars) + ")")
            run_server(hostname, port, args.name, args.expander, self.to_hex(args.address), int(args.num_lines), int(args.num_chars), self.description)
            return True
        elif args.command == 'register' and (args.expander is not None) and (args.address is not None):
            print("register " + self.packagename  + " on " + hostname + ":" + str(port) + " (LCD " + str(args.num_lines)  + "/" + str(args.num_chars) + ") and starting it")
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename, entrypoint=self.entrypoint, hostname=hostname, port=port, verbose=verbose, name=args.name, expander=args.expander, address=args.address, num_lines=args.num_lines, num_chars=args.num_chars)
            self.unit.register(hostname, port, unit)
            return True
        else:
            return False

    def to_hex(self, hexString: str) -> int:
        if hexString.startswith("0x"):
            return int(hexString, 16)
        else:
            return int(hexString)


def main():
    DhtApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()
