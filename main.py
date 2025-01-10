import tkinter as tk  # for handling windows, frames, and labels
from PIL import Image, ImageTk  # for handling images
import pygame # for handling audio

    # Colors to save: #B88458 Brown (background), #422638 Dark Purple(misc use),  #EB9144 Orange(fore color)

# Initialize pygame for audio
pygame.mixer.init()

# Initialize music playing state
music_playing = False

# Load the music file and sound effects
pygame.mixer.music.load("assets/sounds/background_music.mp3")  # Replace with your music file
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
sound_effect = pygame.mixer.Sound("assets/sounds/sound_effect.wav")  # Replace with your sound effect file
sound_effect.set_volume(0.8)  # Set sound effect volume (0.0 to 1.0)

#  Custom Start button class
class ImageButtonStart(tk.Label):
    def __init__(self, master, image_normal, image_pressed, command=None, **kwargs):
        super().__init__(master, **kwargs)

        # Load images
        self.image_normal = ImageTk.PhotoImage(Image.open(image_normal))
        self.image_pressed = ImageTk.PhotoImage(Image.open(image_pressed))

        # Set initial image
        self.configure(image=self.image_normal)

        # Store the command to execute on click
        self.command = command

        # Bind mouse events
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        # Change the image to the pressed image
        self.configure(image=self.image_pressed)

    def on_release(self, event):
        # Revert to the normal image
        self.configure(image=self.image_normal)

        # Execute the command if provided
        if self.command:
            self.command()

# Function to display text one letter at a time
def animate_text(selected_text):
    global position_index
    global writing
    global text_speed
    full_text = dialogs[selected_text]  # Get the selected string from the dictionary
    if position_index < len(full_text):
        writing = True
        displayed_text.set(full_text[:position_index + 1])  # Update the displayed text
        position_index += 1
        root.after(text_speed, lambda: animate_text(selected_text))  # Schedule the next update
    else:
        writing = False
        text_speed = 40 #  If the dialog is finished writing, reset text speed


# Function to start the animation
def start_dialog_animation(selected_text):
    global position_index
    position_index = 0  # Reset the index
    animate_text(selected_text)

#  Function to toggle mute

def toggle_mute():
    global is_muted, music_playing
    is_muted = not is_muted
    update_button() #function to update button image

    # mute of unmute sound
    if is_muted:
        pygame.mixer.music.set_volume(0) # mute music
    else:
        pygame.mixer.music.set_volume(0.5)

def play_sound_effect():
    if not is_muted:
        sound_effect.play()

def start_music():
    global music_playing
    if not music_playing:
        pygame.mixer.music.play(-1) # loop the music
        music_playing = True

def stop_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        music_playing = False

def update_button():
    if is_muted:
        mute_button.config(image=ui["sound_button_muted"])
        # placeholder - mute sound here
    else:
        mute_button.config(image=ui["sound_button"])
        # placeholder - mute sound here

def reset_game():
    global ingredient_a
    global ingredient_b
    #global waiting_to_start
    global start_button_visible
    ingredient_a = False
    ingredient_b = False
    #waiting_to_start = True
    start_button_visible = True
    change_scene("scene_00")
    custom_start_button.place(x=900, y=600)
    label_dialog.place_forget()

# Start Button Click Event
def on_start_button_click():
    global start_button_visible
    custom_start_button.place_forget()
    play_sound_effect()
    start_button_visible = False
    change_scene("scene_01")
    label_dialog.place(x=300, y=630, width=700)
    start_dialog_animation("dialog_01")
    return

def button_a_click():
    global ingredient_a  # Import variable
    play_sound_effect()  # play click sound
    ingredient_a = True  # Set A to True
    change_scene("scene_04")  # Change to image 4
    start_dialog_animation("dialog_04")
    btnB.place_forget()  # hide button
    btnA.place_forget()  # hide button

def button_b_click():
    global ingredient_b
    play_sound_effect()  # play click sound
    ingredient_b = True
    change_scene("scene_04")
    start_dialog_animation("dialog_04")
    btnA.place_forget()
    btnB.place_forget()


# Function to change the image
def change_scene(image_name):
    global current_scene
    if image_name in scene_images:
        image_label_scene.config(image=scene_images[image_name])
        current_scene = image_name  # Update the current image name
        print(f"Current image: {current_scene}")



# Start of main code

# Variable to track ingredient selection
ingredient_a = False
ingredient_b = False

# Set speed for text animation
text_speed = 40

# Variable to track if writing animation
writing = False

# Variable to track if sound muted
is_muted = False

# Variable to track the currently displayed scene
current_scene = None

# Variable to track writing animation position in the string
position_index = 0

# Creating main tkinter window
root = tk.Tk()  # Creating the main application window
root.geometry("1280x720")  # Set window size
root.configure(bg="#B88458")  # Set window background color
root.title("Soup Py")  # Set window title
root.resizable(False, False)  # Disable resizing window

# Start music
start_music()


# TK variable: Load scene images and store in a dictionary
scene_images = {
    "scene_00": ImageTk.PhotoImage(Image.open("assets/images/scene_00.png")),
    "scene_01": ImageTk.PhotoImage(Image.open("assets/images/scene_01.png")),
    "scene_02": ImageTk.PhotoImage(Image.open("assets/images/scene_02.png")),
    "scene_03": ImageTk.PhotoImage(Image.open("assets/images/scene_03.png")),
    "scene_04": ImageTk.PhotoImage(Image.open("assets/images/scene_04.png")),
    "scene_05": ImageTk.PhotoImage(Image.open("assets/images/scene_05.png")),
    "scene_06": ImageTk.PhotoImage(Image.open("assets/images/scene_06.png")),
    "scene_07": ImageTk.PhotoImage(Image.open("assets/images/scene_07.png")),
    "scene_08": ImageTk.PhotoImage(Image.open("assets/images/scene_08.png"))
}

# TK variable: Load user interface images and store in a dictionary
ui = {
    "start_button": ImageTk.PhotoImage(Image.open("assets/images/button_00.png")),
    "start_button_clicked": ImageTk.PhotoImage(Image.open("assets/images/button_01.png")),
    "sound_button": ImageTk.PhotoImage(Image.open("assets/images/button_02.png")),
    "sound_button_muted": ImageTk.PhotoImage(Image.open("assets/images/button_03.png"))

}

# TK variable: dialog dictionary
dialogs = {
    "dialog_00": "The quick brown fox The quick brown fox 00",
    "dialog_01": "Jumps over the lazy dog The quick brown fox 01",
    "dialog_02": "The quick brown fox The quick brown fox 02",
    "dialog_03": "Jumps over the lazy dog The quick brown fox 03",
    "dialog_04": "The quick brown fox The quick brown fox 04",
    "dialog_05": "jumps over the lazy dog The quick brown fox 05",
    "dialog_06": "The quick brown fox The quick brown fox 06",
    "dialog_07": "The quick brown fox The quick brown fox 07",
    "dialog_08": "Jumps over the lazy The quick brown fox dog 08",
    "dialog_09": "The quick brown fox The quick brown fox 09",
    "dialog_10": "Jumps over the lazy dog The quick brown fox 10",
    "dialog_11": "The quick brown fox The quick brown fox 11",
    "dialog_12": "jumps over the lazy dog The quick brown fox 12",
    "dialog_13": "The quick brown fox The quick brown fox 13"
}

# TK variable to hold text to be animated
displayed_text = tk.StringVar()

# Create frame to contain main game. set size, color, and remove padding
frame = tk.Frame(root, width=1280, height=720, bg="#B88458", borderwidth=0, highlightthickness=0)
frame.place(x=0, y=0)  # set frame position

# Create label to display scene images. # Set color, Remove padding
image_label_scene = tk.Label(frame, bg="#B88458", borderwidth=0, highlightthickness=0)
image_label_scene.place(x=0, y=0)  # set scene position

# Create Sound toggle button
mute_button = tk.Button(
    root,
    image=ui["sound_button"],
    command=toggle_mute,
    borderwidth=0,
    highlightthickness = 0, # Removes border on focus
    bg="#5f5f5f", # Background for transparency if needed
    activebackground= "#5f5f5f",
    relief="flat"
)
mute_button.place(x=1200, y=75)

# Create label to display animated dialog
label_dialog = tk.Label(
    frame,
    textvariable=displayed_text,
    font=("Arial", 24),
    bg="#422638",  # Dark Purple
    fg="#EB9144",  # Orange
    height=2,
    anchor="nw",
    justify="left",
)
#422638

# Create buttons for ingredients, but don't place them yet.
btnA = tk.Button(frame, text="", background="#B88458", foreground="#B88458", width=15, height=2, font=("Arial", 12), command=lambda: button_a_click())
btnB = tk.Button(frame, text="", background="#B88458", foreground="#B88458", width=15, height=2, font=("Arial", 12), command=lambda: button_b_click())


# Create the custom start button
custom_start_button = ImageButtonStart(
    root,
    image_normal="assets/images/button_00.png",   # Replace with your image file
    image_pressed="assets/images/button_01.png",  # Replace with your image file
    command=on_start_button_click,
    bg="#5f5f5f"  # Background for transparency if needed
)
custom_start_button.place(x=900, y=600)
start_button_visible = True


# Display first scene image (title screen)
change_scene("scene_00")


# Handle click events on the background
def on_background_click(event):
    global writing
    global text_speed

    if start_button_visible:
        return

    if writing:
        text_speed = 2
    else:

        if current_scene == "scene_01":
            play_sound_effect()  # play click sound
            change_scene("scene_02")
            start_dialog_animation("dialog_02")
            return

        if current_scene == "scene_02":
            play_sound_effect()  # play click sound
            change_scene("scene_03")
            start_dialog_animation("dialog_03")
            btnA.place(x=400, y=430)  # Set Button A position
            btnB.place(x=780, y=430)  # Set Button B position
            return

        if current_scene == "scene_03":  # No click function here. press ingredient button inst ead.
            return

        if current_scene == "scene_04":
            play_sound_effect()  # play click sound
            change_scene("scene_05")
            start_dialog_animation("dialog_05")
            return

        if current_scene == "scene_05":
            play_sound_effect()  # play click sound
            global ingredient_a
            if ingredient_a:
                change_scene("scene_06")
                start_dialog_animation("dialog_06")
            else:
                global ingredient_b
                if ingredient_b:
                    change_scene("scene_07")
                    start_dialog_animation("dialog_07")
            return

        if current_scene == "scene_06":
            play_sound_effect()  # play click sound
            change_scene("scene_08")
            label_dialog.place_forget()
            return

        if current_scene == "scene_07":
            play_sound_effect()  # play click sound
            change_scene("scene_08")
            label_dialog.place_forget()
            return

        if current_scene == "scene_08":
            play_sound_effect()  # play click sound
            reset_game()
            return



# Bind click events for the
root.bind("<Button-1>", on_background_click)  # Left-click on the window's background
root.bind("<Button-2>", on_background_click)  # Left-click on the window's background

root.mainloop()
