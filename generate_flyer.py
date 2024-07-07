import yaml
import qrcode
from jinja2 import Environment, FileSystemLoader

def read_yaml_header_from_md(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('---')
        yaml_content = yaml.safe_load(content[1]) if len(content) > 2 else {}
        return yaml_content if yaml_content is not None else {}

def read_yaml_from_file(file_path):
    with open(file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
        return yaml_content if yaml_content is not None else {}

def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    return file_path

index_md_data = read_yaml_header_from_md('index.md')

config_data = read_yaml_from_file('_config.yml')

flyer_data = read_yaml_from_file('flyer.yml')

combined_data = {**index_md_data, **config_data, **flyer_data}

registration_qr_path = generate_qr_code(combined_data['registration_link'], 'workshop_assets/img/registration_qr.png')
workshop_website_qr_path = generate_qr_code(combined_data['workshop_website'], 'workshop_assets/img/workshop_website_qr.png')

combined_data['registration_qr_path'] = registration_qr_path
combined_data['workshop_website_qr_path'] = workshop_website_qr_path

env = Environment(loader=FileSystemLoader('.'), autoescape=True)
template = env.get_template('flyer_template.html')
output = template.render(combined_data)

with open('workshop_flyer.html', 'w') as output_file:
    output_file.write(output)

print("Flyer generated successfully.")