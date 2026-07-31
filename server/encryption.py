

def encrypt(inputText,N,D):
    """ Takes in input text and performs transformation of N ascii shifts and D direction
    to return encrypted string. This function allows 32-126 compared to our HW version."""

    # Reverse the input text 
    new_text=''
    # index starts at last ch, stops at 0 (since exclusive), step of -1
    for i in range(len(inputText)-1,-1,-1):
        # Add to reversed new string
        new_text += inputText[i]

    # Shift ASCII by "N" positions and "D" direction
    encrypted_string =''
    for ch in new_text:

        # shift everything down to 0 based (subtract 32) for easier analysis
        # make so pos 32 is at 0
        start_pos= ord(ch) -32
        shifted_pos = start_pos + (D * N)

        # we have 95 total values, divide by 95 and get remainder to help cycle around if needed
        shifted_pos = shifted_pos % 95

        # add 32 back for correct ascii code
        encrypted_string += chr(shifted_pos+32)

    return encrypted_string
