package com.dzl;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.dzl.entity.Message;
import com.dzl.mapper.MessageMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import javax.annotation.Resource;
import java.util.List;

@SpringBootTest
class YiqingApplicationTests {

	@Resource
	MessageMapper messageMapper;

	@Test
	void contextLoads() {
//		String msg = messageMapper.selectOneMsg();
//		System.out.println("message:"+msg);
//		Message l = messageMapper.selectOne(null);
//		System.out.println(l.toString());

		QueryWrapper<Message> queryWrapper = new QueryWrapper<>();
		String sql = "select max(time) from message";
		queryWrapper.inSql("time",sql);
		Message l = messageMapper.selectOne(queryWrapper);
		System.out.println(l.toString());
		//("select *\n" +
		//            "from message\n" +
		//            "where time in (select max(time) from message)")
	}

}
