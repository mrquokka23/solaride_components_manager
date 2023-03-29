import PySimpleGUI as sg
from sheets import get_data, update_data
from camera import get_camera

def main():
    sg.theme('DarkAmber')
    data = get_data()
    components_column = [
        [
            sg.Text('Components'),
        ],
        [
            sg.Text('Search'), sg.Input('', enable_events=True ,key='-SEARCH-')
        ],
        [
            sg.Listbox(values=[data[i]['MFGPN'] for i in data], size=(15, 20), enable_events=True, key='-MFGPN-', expand_x=True)
        ],
        [
            sg.Button('Edit', key='-EDIT-'),
            sg.Button('Delete', key='-DELETE-')
        ]

    ]
    add_component_column = [
        [
                sg.Text(key='-PART1-')
        ],
        [
                sg.Text(key='-PART2-')
        ],
        [
                sg.Text(key='-PART3-')
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text('Add a component')
        ],
        [
            sg.Text('MFGPN'),sg.Input('', key='-MFGPNIN-')
        ],
        [
            sg.Text('Quantity'),sg.Input('', key='-QUANTITY-')
        ],
        [
            sg.Text('Category'), sg.Input('', key='-CATEGORY-')
        ],
        [
            sg.Text('Orders'), sg.Input('', key='-ORDERS-')
        ],
        [
            sg.Text('Location'), sg.Input('', key='-LOCATION-')
        ],
        [
            sg.Button('Submit', key='-SUBMIT-'),
            sg.Button('Add with camera', key='-CAMERA-')
        ]

    ]
    layout = [
                [
                    sg.Column(components_column),
                    sg.VSeperator(),
                    sg.Column(add_component_column)
                ]
            ]
    edit_layout = [
        [
            sg.Text(key='-EDITPART-')
        ],
        [
            sg.Text('Quantity'),sg.Input('', key='-QUANTITYEDIT-')
        ],
        [
            sg.Text('Category'), sg.Input('', key='-CATEGORYEDIT-')
        ],
        [
            sg.Text('Location'), sg.Input('', key='-LOCATIONEDIT-')
        ],
        [
            sg.Button('Save', key='-SAVE-EDIT-')
        ]
    ]
    window = sg.Window('Component Manager', layout)
    while True:
        event, values = window.read(close=False)
        if event == '-SUBMIT-':
            success = False
            for k in range(len(data)):
                if data[k+1]['MFGPN'] == values['-MFGPNIN-']:
                    data[k+1]['QUANTITY'] += int(values['-QUANTITY-'])
                    data[k+1]['CATEGORY'] = values['-CATEGORY-']
                    data[k+1]['ORDERS'].append(tuple(values['-ORDERS-'].split(':')))
                    data[k+1]['LOCATION'] = values['-LOCATION-']
                    update_data(data)
                    data = get_data()
                    success = True
                    window['-MFGPNIN-'].update('')
                    window['-QUANTITY-'].update('')
                    window['-CATEGORY-'].update('')
                    window['-ORDERS-'].update('')
                    window['-LOCATION-'].update('')
                    break
            if not success:
                data[len(data)+1] = {'MFGPN': values['-MFGPNIN-'], 'QUANTITY': values['-QUANTITY-'], 'CATEGORY': values['-CATEGORY-'], 'ORDERS': [tuple([values['-ORDERS-'].split(':')[0], int(values['-ORDERS-'].split(':')[1])])], 'LOCATION': values['-LOCATION-']}
                window['-MFGPN-'].update(values=[data[i]['MFGPN'] for i in data])
                update_data(data)
        if event == '-SEARCH-':
            window['-MFGPN-'].update(values=[data[i]['MFGPN'] for i in data if values['-SEARCH-'].lower() in data[i]['MFGPN'].lower()])

        if event == '-MFGPN-':
            for i in range(len(data)):
                if data[i+1]['MFGPN'] == values['-MFGPN-'][0]:
                    window['-PART1-'].update(f'Part: {data[i+1]["MFGPN"]}')
                    window['-PART2-'].update(f'Quantity: {data[i+1]["QUANTITY"]}')
                    window['-PART3-'].update(f'Location: {data[i+1]["LOCATION"]}')
                    
        
        if event == '-CAMERA-':
            mfgpn = get_camera()
            if mfgpn != None:
                window['-MFGPNIN-'].update(mfgpn['MFGPN'])
                window['-QUANTITY-'].update(mfgpn['QUANTITY'])
                window['-ORDERS-'].update(f"{mfgpn['FROM']}:{mfgpn['ORDER']}")
                

        if event == '-EDIT-' and values['-MFGPN-']:
            editwindow = sg.Window('Edit', edit_layout, finalize=True)
            
            for i in range(len(data)):
                    if data[i+1]['MFGPN'] == values['-MFGPN-'][0]:
                        editwindow['-EDITPART-'].update(f'Edit: {data[i+1]["MFGPN"]}')
                        editwindow['-QUANTITYEDIT-'].update(data[i+1]['QUANTITY'])
                        editwindow['-CATEGORYEDIT-'].update(data[i+1]['CATEGORY'])
                        editwindow['-LOCATIONEDIT-'].update(data[i+1]['LOCATION'])
                        
            while True:
                editevent, editvalues = editwindow.read(close=False)
                if editevent == sg.WIN_CLOSED:
                    editwindow = None
                    break
                print(editevent)
                if editevent == '-SAVE-EDIT-':
                    for i in range(len(data)):
                        if data[i+1]['MFGPN'] == values['-MFGPN-'][0]:
                            data[i+1]['QUANTITY'] = int(editvalues['-QUANTITYEDIT-'])
                            data[i+1]['CATEGORY'] = editvalues['-CATEGORYEDIT-']
                            data[i+1]['LOCATION'] = editvalues['-LOCATIONEDIT-']
                            update_data(data)
                            break
                    editwindow.close()
                    editwindow = None
                    window['-MFGPN-'].update(values=[data[i]['MFGPN'] for i in data])
                    for i in range(len(data)):
                        if data[i+1]['MFGPN'] == values['-MFGPN-'][0]:
                            window['-PART-'].update(f'Part: {data[i+1]["MFGPN"]} - Quantity: {data[i+1]["QUANTITY"]} - Location: {data[i+1]["LOCATION"]}')
                    break
                    
        elif event == '-EDIT-' and not values['-MFGPN-']:
            sg.popup('Please select a component to edit')

        if event == '-DELETE-' and values['-MFGPN-']:
            cg = sg.popup_ok_cancel('Are you sure you want to delete this component?', title='Delete')
            if cg == 'OK':
                for i in range(len(data)):
                    if data[i+1]['MFGPN'] == values['-MFGPN-'][0]:
                        del data[i+1]
                        update_data(data)
                        data = get_data()
                        window['-MFGPN-'].update(values=[data[i]['MFGPN'] for i in data])
                        break
            else:
                continue
        elif event == '-DELETE-' and not values['-MFGPN-']:
            sg.popup('Please select a component to delete')
        
        if event == sg.WIN_CLOSED:
            break


if __name__ == "__main__":
    main()