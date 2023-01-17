
import toga
import requests
import threading

from consts import *
from toga.style.pack  import *
class PokeDex (toga.App):
    def __init__ (self, title, id):
        toga.App.__init__(self , title, id)
        self.title = title
        self.size = (WIDTH,HEIGTH)
        self.heding = ['Name']
        self.data =[]
        self.offset = 0

        self.response_name = ''

        self.response_description = ''

        self.response_sprite = ''
        
        self.create_elemets()
        self.load_async_data()
        self.validate_previous_command()
    
    def startup (self):
        self.main_window = toga.MainWindow('main', title=self.title,
        
                                             size=self.size)
        information_area = toga.Box(

            children=[self.image_view, self.pokemon_name,self.pokemon_description],
            style=Pack(
                direction= COLUMN,
                alignment= CENTER
            )
        )
        #information_area.add(self.image_view)
        #information_area.add(self.pokemon_name)
        #information_area.add(self.pokemon_description)
        split = toga.SplitContainer()
        split.content = [self.table, information_area]

        self.main_window.content = split
        self.main_window.toolbar.add(self.previous_command, self.next_command)
        
        self.main_window.show()

    def create_elemets(self):
        self.create_table()
        self.create_toolbar()
        self.create_image(NEXT_ICON)
        self.create_label()


    def create_toolbar(self):
        self.create_next_command()
        self.create_previous_command()


    def create_next_command (self ):
        self.next_command = toga.Command(self.next , label='Next',
                                                  icon=NEXT_ICON)


    def create_previous_command (self):
        self.previous_command = toga.Command(self.previous , label='Previous' ,
                                              icon=PREVIOUS_ICON)

    def create_label (self):

        style = Pack(text_align=CENTER)
        self.pokemon_name = toga.Label('Name',style=style)
        
        self.pokemon_description = toga.Label('Description',style=style)

        self.pokemon_name.style.font_size = 20

        self.pokemon_name.style.padding = 25

        self.pokemon_description.style.font_size = 10


    def create_image (self,path, width = 200, height=200):
        image = toga.Image(path)
        style = Pack(width=width, height=height)
        self.image_view = toga.ImageView(image, style=style)


    def create_table (self):
        self.table = toga.Table(self.heding, data=self.data, on_select=self.select_element)


    def load_async_data (self):
        self.data.clear()
        self.image_view.image = None
        self.pokemon_name.text = 'loading...'
        self.pokemon_description.text = ''
        thread = threading.Thread(target=self.load_data)
        thread.start()
        thread.join()
        self.table.data = self.data

    def load_async_pokemon(self, pokemon):
        thread = threading.Thread(target=self.load_pokemon, args=[pokemon])
        thread.start()
        thread.join()

        self.image_view.image = toga.Image(self.response_sprite)
        self.pokemon_name.text = self.response_name
        self.pokemon_description.text = self.response_description



    def load_pokemon (self, pokemon):
        path = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon)

        response = requests.get(path)
        if response:
            result = response.json()

            self.response_name = result['forms'][0]['name']
            abilities = []

            for ability in result['abilities']:
                name_ability = ability['ability']['name']
                abilities.append(name_ability)

            self.response_sprite = result['sprites']['front_default']

            self.response_description = ''.join(abilities)
            print(self.response_description)

            

            

    def load_data (self):
        
        
        path = 'https://pokeapi.co/api/v2/pokemon-form?offset={}&limit=20'.format(self.offset)

        response = requests.get(path)
        
        if response:
            result = response.json()

            for pokemon in result['results']:
                name = pokemon['name']
                self.data.append(name)

    
        
        
    #CALLBACKS 

    def next (self, widget):
        self.offset += 1
        self.handler_command(widget)

    def previous (self, widget):
        self.offset -= 1
        self.handler_command(widget)
    
    def handler_command(self, widget):
        widget.enabled = False

        self.load_async_data()

        widget.enabled = True

        self.validate_previous_command()

       
    def validate_previous_command(self):
        self.previous_command.enabled = not self.offset == 0

  
    
    def select_element(self, widget, row):
        if row:
             self.load_async_pokemon(row.name)
if __name__ == '__main__':
    pokedex = PokeDex('PokeDex', 'com.codigofacilito.PokeDex')

    pokedex.main_loop()
