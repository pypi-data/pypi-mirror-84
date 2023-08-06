import ui

from ui3.sfsymbol import *


class SymbolSource:
    
    symbols_per_page = 20
  
    def __init__(self, root, tableview):
        self.tableview = tableview
        tableview.row_height = 50
        self.weight = THIN
        
        with open('sfsymbolnames.txt', 'r') as fp:
            all_lines = fp.read()    
        raw = all_lines.splitlines()
        
        restricted_prefix = 'Usage restricted'
        
        self.symbol_names = []
        for i, symbol_name in enumerate(raw):
            if raw[i].startswith(restricted_prefix): continue
            if i+1 == len(raw): continue
            value = symbol_name
            if raw[i+1].startswith(restricted_prefix):
                value = 'R ' + value
            self.symbol_names.append(value)

        self.index = 0
        self.update_list_to_display()
        
        self.prev_button = ui.ButtonItem(
          tint_color='black',
          image=SymbolImage('arrow.left', 8, weight=THIN),
          enabled=False,
          action=self.prev,
        )
        self.to_start_button = ui.ButtonItem(
          tint_color='black',
          image=SymbolImage('arrow.left.to.line', 8, weight=THIN),
          enabled=False,
          action=self.to_start,
        )
        self.next_button = ui.ButtonItem(
          tint_color='black',
          image=SymbolImage('arrow.right', 8, weight=THIN),
          enabled=True,
          action=self.next,
        )
        self.to_end_button = ui.ButtonItem(
          tint_color='black',
          image=SymbolImage('arrow.right.to.line', 8, weight=THIN),
          enabled=True,
          action=self.to_end,
        )
        self.weight_button = ui.ButtonItem(
          tint_color='black',
          title='Thin',
          enabled=True,
          action=self.change_weight,
        )
      
        root.left_button_items = [
            self.to_start_button,
            self.prev_button]
        root.right_button_items = [
            self.to_end_button, 
            self.next_button, 
            self.weight_button]
        
    def update_list_to_display(self):
        self.data_list = []
        for i in range(self.index, self.index+self.symbols_per_page):
            self.data_list.append(self.symbol_names[i])
        
    def next(self, sender):
        self.index += self.symbols_per_page
        if self.index + self.symbols_per_page >= len(self.symbol_names):
            self.index = len(self.symbol_names) - self.symbols_per_page - 1
            self.next_button.enabled = False
            self.to_end_button.enabled = False
        self.prev_button.enabled = True
        self.to_start_button.enabled = True
        self.update_list_to_display()
        self.tableview.reload()
        
    def to_end(self, sender):
        self.index = len(self.symbol_names) - self.symbols_per_page - 1
        self.next_button.enabled = False
        self.to_end_button.enabled = False
        self.prev_button.enabled = True
        self.to_start_button.enabled = True
        self.update_list_to_display()
        self.tableview.reload()
        
    def prev(self, sender):
        self.index -= self.symbols_per_page
        if self.index <= 0:
            self.index = 0
            self.prev_button.enabled = False
            self.to_start_button.enabled = False
        self.next_button.enabled = True
        self.to_end_button.enabled = True
        self.update_list_to_display()
        self.tableview.reload()
        
    def to_start(self, sender):
        self.index = 0
        self.prev_button.enabled = False
        self.to_start_button.enabled = False
        self.next_button.enabled = True
        self.to_end_button.enabled = True
        self.update_list_to_display()
        self.tableview.reload()
        
    def change_weight(self, sender):
        titles = ['Ultralight', 'Thin', 'Light', 'Regular', 'Medium', 'Semibold', 'Bold', 'Heavy', 'Black']
        self.weight += 1
        if self.weight > BLACK:
            self.weight = ULTRALIGHT
        self.weight_button.title = titles[self.weight-1]
        self.tableview.reload()
        
    def tableview_number_of_rows(self, tableview, section):
        return len(self.data_list)
        
    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.selectable = False
        cell.background_color='black'
        
        symbol_name = self.data_list[row]
        tint_color = 'white'
        if symbol_name.startswith('R '):
            symbol_name = symbol_name[2:]
            tint_color = 'orange'
        symbol_image = SymbolImage(symbol_name, 
        point_size=14, weight=self.weight, scale=SMALL)

        button = ui.Button(
            tint_color=tint_color,
            title='   '+symbol_name,
            font=('Fira Mono', 14),
            image=symbol_image,
            frame=cell.content_view.bounds,
            flex='WH',
            action=self.copy_to_clipboard,
            #enabled=False,
        )

        cell.content_view.add_subview(button)

        return cell

    def copy_to_clipboard(self, sender):
        clipboard.set(sender.title[3:])
        dialogs.hud_alert('Copied')
  
    def textfield_did_change(self, textfield):
        search_text = textfield.text.strip().lower()
        if search_text == '':
            self.update_list_to_display()
            textfield.end_editing()
        else:
            self.data_list = list(fuzzyfinder(search_text, self.symbol_names))
        self.tableview.reload()

def fuzzyfinder(input, collection, accessor=lambda x: x, sort_results=True):
    suggestions = []
    input = str(input) if not isinstance(input, str) else input
    pat = '.*?'.join(map(re.escape, input))
    pat = '(?=({0}))'.format(pat)
    regex = re.compile(pat, re.IGNORECASE)
    for item in collection:
        r = list(regex.finditer(accessor(item)))
        if r:
            best = min(r, key=lambda x: len(x.group(1)))
            suggestions.append((len(best.group(1)), best.start(), accessor(item), item))
    if sort_results:
        return (z[-1] for z in sorted(suggestions))
    else:
        return (z[-1] for z in sorted(suggestions, key=lambda x: x[:2]))
  
root = ui.View()
  
symbol_table = ui.TableView(
    background_color='black',
    frame=root.bounds, flex='WH',
)
data_source = symbol_table.data_source = SymbolSource(root, symbol_table)

search_field = ui.TextField(
    frame=(8,8, root.width-16, 40),
    flex='W',
    clear_button_mode='always',
    delegate=data_source,
)
symbol_table.y = search_field.height + 16
symbol_table.height -= (search_field.height + 16)

root.add_subview(search_field)
root.add_subview(symbol_table)

#symbol_table.present()
root.present('fullscreen')
