"use client";
// redux
import { useSelector } from "react-redux";
import { IUserState } from "@/app/userSlice";
import DefaulMenu from "./defaultMenu";
import LoginMenu from "./loginMenu";
import { useDispatch } from "react-redux";
import { UserController } from "@/api/userApi";

export default function Navbar() {
  const userController = new UserController();

  const dispatch = useDispatch();
  userController.checkAuth(dispatch);
  const user: IUserState = useSelector((state: any) => state.user);
  return user && user.isAuth ? <LoginMenu /> : <DefaulMenu />;
}
