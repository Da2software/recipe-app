"use client";
// redux
import { useSelector } from 'react-redux';
import { IUserState } from '@/app/userSlice';
import DefaulMenu from './defaultMenu';
import LoginMenu from './loginMenu';

export default function Navbar(){
    const user: IUserState = useSelector((state: any)=> state.user);
    return user && user.isAuth ? <DefaulMenu /> : <LoginMenu />;
}