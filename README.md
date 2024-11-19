## Required Packages

To run this project, you need to install the following Python packages:

1. **RPi.GPIO**: This package is used to control the GPIO pins on the Raspberry Pi.
    ```sh
    pip install RPi.GPIO
    ```

2. **rpi_lcd**: This package is used to control the LCD display connected to the Raspberry Pi.
    ```sh
    pip install rpi_lcd
    ```

3. **telepot**: This package is used to send notifications via a bot.
    ```sh
    pip install telepot
    ```
4. **dotenv**: This package is used to load environment variables from a .env file.
    ```sh
    pip install python-dotenv
    ```
5. **gpiozero**: This package is used to control the motion sensor.
    ```sh
    pip install gpiozero
    ```

## Enabling I2C Interface

To enable the I2C interface on the Raspberry Pi, follow the steps below:

1. Run the following command to open the Raspberry Pi configuration tool:
    ```sh
    sudo raspi-config
    ```
2. Select `Interfacing Options` from the menu.
3. Select `I2C` from the list of interfaces.
4. Choose `Yes` when asked if you want to enable the I2C interface.
5. Reboot the Raspberry Pi to apply the changes.

## Setting Up the .env File

To use the Telegram bot in this project, you need to create a `.env` file in the project directory with contents as in .env.example file. Replace the placeholders with your actual values.