from mailjet_rest import Client
from django.conf import settings



def reset_password_email(email, hash):
	mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
	data = {
		'Messages': [{
			"From": {
				"Email": "norma.contreras@nilaconsulting.com.mx",
				"Name": "Licitamex"
			},
			"To": [{
				"Email": email,
				"Name": "You"
			}],
			"Subject": "Restablecer contraseña",
			"HTMLPart": f"""<h3>usted a solicitado cambiar contraseña.</h3>
			<br/>por favor da click en el link para cambiar tu contraseña<br/>
			<a href=\"https://consultalicitamex.com/account/set-new-password/?email={email}&hash={hash}\">consultalicitamex</a>"""
		}]
	}
	mailjet.send.create(data=data)



def registro_exitoso_email(email):
	mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
	data = {
		'Messages': [{
			"From": {
				"Email": "norma.contreras@nilaconsulting.com.mx",
				"Name": "Licitamex"
			},
			"To": [{
				"Email": email,
				"Name": "You"
			}],
			"Subject": "Registro Exitoso",
			"HTMLPart": f"""<h3>Gracias por registrarte en LICITAMEX.</h3>
			<br/>Empieza a usar tu cuenta aqui.<br/>
			<a href=\"https://consultalicitamex.com/\">consultalicitamex</a>"""
		}]
	}
	mailjet.send.create(data=data)


def invitacion_usuario_email(email, group):
	mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
	data = {
		'Messages': [{
			"From": {
				"Email": "norma.contreras@nilaconsulting.com.mx",
				"Name": "Licitamex"
			},
			"To": [{
				"Email": email,
				"Name": "You"
			}],
			"Subject": f"invitacion {group}",
			"HTMLPart": f"""<h3>Has sido invitado al grupo {group}</h3>
			<br/>Empieza a usar tu cuenta aqui.<br/>
			<a href=\"https://consultalicitamex.com/\">ir a mi cuenta</a>"""
		}]
	}
	mailjet.send.create(data=data)