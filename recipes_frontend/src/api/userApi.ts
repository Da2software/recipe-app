import { ResStatus } from "./common";
import { IUserState, addUser } from "@/app/userSlice";
import { changeAuth } from '@/app/userSlice';


export class UserController {
    baseUrl: string = process.env.USERS_API + "/auth/";
    
    async checkAuth(dispatch: any): Promise<any> {
        const res = await fetch(this.baseUrl, {
            method: "GET",
            credentials: "include"
        })
        if (res.ok) {
            const body: any = res.body;
            const userRes: IUserState = {
                username: body["user_name"],
                email: body["email"],
                isAuth: true,
            };
            dispatch(addUser(userRes));
        } else {
            console.warn("User not authenticated!");
        }
    };

    async login(username: string, password: string, dispatch: any): Promise<ResStatus> {
        const response = await fetch(process.env.USERS_API + "/auth/token", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                username: username,
                password: password,
            }),
        });

        if (response.ok) {
            this.checkAuth(dispatch);
            return new ResStatus(true, "Login Successful!");
        } else {
            return new ResStatus(false, "User or Password incorrect!");
        }
    }
    async logout(dispatch: any): Promise<any>{
        fetch(process.env.USERS_API + "/auth/logout", {
            method: "GET",
            credentials: "include",
          }).then((res) => {
            if (res.ok) {
              dispatch(changeAuth(false));
            } else {
              console.warn("Can't logout!");
            }
          });
    }
}