export interface IStatus{
    status: boolean,
    message: string,
    [propName: string]: any
}
export class ResStatus implements IStatus{
    status: boolean=true;
    message: string="OK";
    [propName: string]: any;
    constructor(status = true, message = "OK"){
        this.status = status;
        this.message = message;
    }
}