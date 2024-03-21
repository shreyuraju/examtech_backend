import os
from PIL import Image
from pix2text import Pix2Text

def process_equations(equations):
    if equations.startswith('\\begin{array}'):
        # Directly render the equation
        return equations
    elif '\n' not in equations.strip():
        # Single-line equation, wrap it in \[ \]
        return f'\\[ {equations} \\]'
    else:
        return equations

def read_screenshot():
    # Set the file name
    file_name = "screenshot.png"
    # Get the current directory
    current_directory = os.getcwd()
    # Append the subdirectory name
    current_directory = os.path.join(current_directory, 'uploads')
    # Construct the full path
    file_path = os.path.join(current_directory, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the image file
        image = Image.open(file_path)
        try:
            from pix2text import Pix2Text, merge_line_texts
            # img_fp = './en1.jpg'
            
            # p2t = Pix2Text()                                          #
            # outs = p2t.recognize_text(image)                       #          text only
            # print(outs)                                               #
            
            p2t = Pix2Text()                                                                                                                    #
            outs = p2t.recognize(image, resized_shape=608, return_text=True)  # You can also use `p2t(img_fp)` to get the same result            #        multi line code
            print(outs)                                                                                                                           #  
            return outs
        
            # p2t = Pix2Text()
            # equations = p2t.recognize_formula(image)
            # processed_equations = process_equations(equations)           #OLD CODE
            # print(processed_equations)
            # return processed_equations
            
            # return render_template('equations.html', equations=processed_equations)
        except Exception as e:
            return f'Error processing image: {str(e)}'
        return image
    else:
        print("File not found")
        return None
