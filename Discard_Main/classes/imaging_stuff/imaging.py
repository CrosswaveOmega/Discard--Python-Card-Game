
def dc(expressionA, expressionB, success_msg="ok", casea_msg="none", caseb_msg="none"):
    passA, passB=False, False
    if(expressionA):
        passA=True
    else:
        print(casea_msg)
    if(expressionB):
        passB=True
    else:
        print(caseb_msg)
    if(passA and passB):
        s=1+2
        #Ok.
    return passA and passB
#We really need to re-organize everything.
def custom_image_scaling(scaled_width, scaled_height, offset_x, offset_y): #Funciton is for scaling a uploaded image
    display_width, display_height=402,  224

    display_x, display_y= 21, 63


    res=dc(scaled_width>=display_width, scaled_height>=display_height, "Test A passed.", "scaled_width is too low.", "scaled_height is too low.")
    if(res):
        print("Test A Passed.")
    res2=dc(offset_x<=display_x,offset_y<=display_y , "Test B passed.", "offset_x is too high.", "offset_y is too high.")

    if(res2):
        print("Test B Passed")


    diff_x=display_x-offset_x
    diff_y=display_y-offset_y


    rem_x=scaled_width-diff_x
    rem_y=scaled_height-diff_y

    max_diff_x=scaled_width-display_width
    max_diff_y=scaled_height-display_height
    res3=dc(rem_x>=display_width, rem_y>=display_height , "Test C passed.", "remainder_x is too low.", "remainder_y is too low.")

    if(res3):
        print("Test C Passed")

    print("scaled_size", scaled_width, scaled_height)
    print("scaled_offset", offset_x, offset_y)
    print("display_size", display_width, display_height)
    print("display_offset", display_x, display_y)


    print("diff", diff_x, diff_y)
    print("rem",rem_x, rem_y)
    print("max_diff",max_diff_x, max_diff_y)

    range_x=display_x-max_diff_x
    range_y=display_y-max_diff_y
    print("range",range_x, range_y)
    print("")


#Driver Code.
if __name__ == "__main__":
    custom_image_scaling(521, 288, 0,0)



    print("CLUSTER_TEST.")
    custom_image_scaling(521, 288, 200,0)



    custom_image_scaling(521, 288, -98,0)
    custom_image_scaling(521, 288, 21,0)
    custom_image_scaling(521, 288, -150,0)
    custom_image_scaling(521, 288, 50,0)
    custom_image_scaling(521, 288, 521,0)
    custom_image_scaling(521, 288, 521-21,0)

    custom_image_scaling(521, 288, -521+22,0)
    custom_image_scaling(521, 288, -521,0)
