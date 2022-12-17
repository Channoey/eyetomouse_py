package com.dzl.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.dzl.common.Result;
import com.dzl.entity.Message;
import com.dzl.entity.Sign;
import com.dzl.mapper.ManageMapper;
import com.dzl.mapper.MessageMapper;
import com.dzl.service.IUserService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

@RestController
public class EyeController {

    @Resource
    private IUserService userService;

    @Resource
    private MessageMapper messageMapper;

    @PostMapping ("/start")
    public int start(@RequestBody Sign sign){
        Process proc;
        try {
            String username = sign.getUser();
            String cmd = "sudo /Users/amateur/opt/anaconda3/envs/ai_study_37/bin/python3.7 " +
                    "/Users/amateur/project/eyetomouse/eyetomouse_py/run.py " + username;
            proc = Runtime.getRuntime().exec(cmd);
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
            return 0;
        } catch (IOException e) {
            e.printStackTrace();
            return -1;
        } catch (InterruptedException e) {
            e.printStackTrace();
            return -2;
        }
    }

    @PostMapping("/test")
    public void test(@RequestBody Sign sign){
        System.out.println("getuser:"+sign.getUser());

    }

    @GetMapping("/message")
    public Result getMessage(){
        QueryWrapper<Message> queryWrapper = new QueryWrapper<>();
        String sql = "select max(time) from message";
        queryWrapper.inSql("time",sql);
        Message msg = messageMapper.selectOne(queryWrapper);
        if(msg.getMessage().equals("-4")){
            return Result.success("-4");
        }
        if(msg.getMessage().equals("-6")){
            return Result.success("-6");
        }
        String res = msg.getMessage()+"        "+msg.getTime();
        System.out.println("res"+res);
        return Result.success(res);
    }

    @PostMapping("/train")
    public Result train(@RequestBody Sign sign){
        Process proc;
        try {
            String username = sign.getUser();
            String cmd = "sudo /Users/amateur/opt/anaconda3/envs/ai_study_37/bin/python3.7 " +
                    "/Users/amateur/project/eyetomouse/eyetomouse_py/train_model.py " + username;
            proc = Runtime.getRuntime().exec(cmd);
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
            return Result.success(0);
        } catch (IOException e) {
            e.printStackTrace();
            return Result.success(-1);
        } catch (InterruptedException e) {
            e.printStackTrace();
            return Result.success(-2);
        }
    }
}
