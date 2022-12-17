package com.dzl.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@TableName("message")
@Data
public class Message {
    @TableId
    private String id;
    private String message;
    private String time;
}
