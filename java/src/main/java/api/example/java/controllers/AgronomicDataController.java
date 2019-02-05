package api.example.java.controllers;

import java.io.IOException;
import java.text.NumberFormat;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import api.example.java.api.ClimateAPIs;
import api.example.java.model.Activity;
import api.example.java.model.ActivityResult;

@Controller
public class AgronomicDataController extends BaseController {
	
	
	@Autowired
	private ClimateAPIs climateAPIs;

	private static Logger logger = LoggerFactory.getLogger(AgronomicDataController.class);

	@GetMapping("/agronomic")
	public String agronomicData(Model model, @RequestParam("data") String dataType, HttpServletRequest request) {
		
		logger.info("Listing agronic {} data"+ dataType);

		List<Activity> acitivities = new ArrayList<Activity>();

		Iterator<ActivityResult> acticityIterator = climateAPIs.getActivityIterator(
				String.format("%s/%s", agronomicApiUri(), dataType)
				, dataType, 
				getAccessTokenFromSession(request));
		while (acticityIterator.hasNext()) {
			ActivityResult activityResult = acticityIterator.next();
			if (activityResult != null) {
				List<Activity> activityList = activityResult.getResults();
				if (activityList != null) {
					acitivities.addAll(activityList);
				}
			}
		}

		model.addAttribute("acitivities", acitivities);
		model.addAttribute("dataType", dataType);
		return "activities";
	}

	@GetMapping("/agronomic-contents")
	public void agronomicDataContent(Model model, @RequestParam("data") String dataType, @RequestParam("id") String id,
			@RequestParam("length") String length, HttpServletRequest request, HttpServletResponse response)
			throws IOException, ParseException {
		logger.info("Fetching contents of agronomic - {} - acitity id - {}  length - {}", dataType, id , length);
		
		Number number = NumberFormat.getNumberInstance(java.util.Locale.US).parse(length);

		response.setContentType("application/zip");
		response.setStatus(HttpServletResponse.SC_OK);
		response.addHeader("Content-Disposition", String.format("attachment; filename=\"%s_%s.zip\"", id, dataType));
		
		ServletOutputStream out = response.getOutputStream();
		
		Iterator<ByteArrayResource> contentItr = climateAPIs.getContentIterator(
				agronomicContentsApiUri(id, dataType),
				dataType, id, number.intValue(),
				getAccessTokenFromSession(request));
		
		while (contentItr.hasNext()) {
			ByteArrayResource buffer = contentItr.next();
			out.write(buffer.getByteArray());
		}
		out.flush();
		out.close();
	}

}
