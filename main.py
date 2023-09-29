import flet as ft

def main(page):
    title_page = ft.Text('Hello, world!')

    chat = ft.Column()

    user_name = ft.TextField(label='Nome do usuário')

    def send_message_tunel(message):
        if message['type'] == 'user_joined':
            chat.controls.append(ft.Text(f'{message["user"]} entrou no chat', color=ft.colors.ORANGE_500, size=12, italic=True))
            chat.update()
            return
        else:
            user_name = message['user']
            message = message['message']
            chat.controls.append(ft.Text(f'{user_name}: {message}'))
            field_message.value = ""
            chat.update()

    def send_message(e):
        page.pubsub.send_all({
            'message': field_message.value, 
            'user': user_name.value,
            'type': 'message'
        })
        field_message.value = ""
        page.update()

    page.pubsub.subscribe(send_message_tunel)

    field_message = ft.TextField(label='Digite sua mensagem')
    button_send = ft.ElevatedButton('Enviar', on_click=(send_message))

    def display_chat(e):
        page.pubsub.send_all({
            'user': user_name.value,
            'type': 'user_joined'
        })
        modal.open = False
        page.add(chat)
        page.remove(initialize_button)
        page.remove(title_page)
        page.add(ft.Row([
            field_message, button_send
        ]))
        page.update()

    modal = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text('Chat Iniciado'),
        content=user_name,
        actions=[
            ft.ElevatedButton('Entrar', on_click=(display_chat)),
        ],
    )

    def signin_chat(e):
        page.dialog = modal
        modal.open = True
        page.update()

    initialize_button = ft.ElevatedButton('Iniciar', on_click=signin_chat)  
    page.add(title_page)
    page.add(initialize_button)


ft.app(target=main, view=ft.WEB_BROWSER, port=5000)
