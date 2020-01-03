import cv2
import streamlit as st

from control import param2func
from utils import get_images_list, load_image, upload_image


def show_logo():
    st.image(load_image("logo.png", "../images"), format="PNG")


def select_image(path_to_images: str, interface_type:str = 'Simple'):
    image_names_list = get_images_list(path_to_images)
    if len(image_names_list) < 1:
        return 0, 0
    else:
        if interface_type == 'Professional':
            image_name = st.sidebar.selectbox("Select an image:", image_names_list + ["Upload my image"])
        else:
            image_name = st.sidebar.selectbox("Select an image:", image_names_list)

        if image_name != 'Upload my image':
            try:
                image = load_image(image_name, path_to_images)
                return 1, image
            except cv2.error:
                return 0, 0
        else:
            try:
                image = upload_image()
                return 1, image
            except cv2.error:
                return 0, 0
            except AttributeError:
                return 2, 0


def show_transform_control(transform_params: dict, n_for_hash: int) -> dict:
    param_values = {"p": 1.0}
    if len(transform_params) == 0:
        st.sidebar.text("Transform has no parameters")
    else:
        for param in transform_params:
            control_function = param2func[param["type"]]
            if isinstance(param["param_name"], list):
                returned_values = control_function(**param, n_for_hash = n_for_hash)
                for name, value in zip(param["param_name"], returned_values):
                    param_values[name] = value
            else:
                param_values[param["param_name"]] = control_function(**param,n_for_hash = n_for_hash)
    return param_values


def show_credentials():
    st.markdown("* * *")
    st.subheader("Credentials:")
    st.markdown(
        (
            "Source: [github.com/IliaLarchenko/albumentations-demo]"
            "(https://github.com/IliaLarchenko/albumentations-demo)"
        )
    )
    st.markdown(
        (
            "Albumentations library: [github.com/albumentations-team/albumentations]"
            "(https://github.com/albumentations-team/albumentations)"
        )
    )
    st.markdown(
        (
            "Image Source: [pexels.com/royalty-free-images]"
            "(https://pexels.com/royalty-free-images/)"
        )
    )


def show_docstring(obj_with_ds):
    st.markdown("* * *")
    st.subheader("Docstring for " + obj_with_ds.__class__.__name__)
    st.text(obj_with_ds.__doc__)
