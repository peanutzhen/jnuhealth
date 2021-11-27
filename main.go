// Author:		https://github.com/peanutzhen
// Contact:		<astzls213@gmail.com>
// License:		GNU GENERAL PUBLIC LICENSE

package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/peanutzhen/jnuhealth/models"
)

var stuInfoReq models.StuInfoReq

func main() {
	flag.StringVar(&stuInfoReq.Jnuid, "jnuid", "", "Your encrtpted jnuId, not 2018xxxxxx, check readme.md to get this.")
	flag.StringVar(&stuInfoReq.IdType, "type", "", "Your idType, check readme.md to get this.")
	flag.Parse()

	if stuInfoReq.Jnuid == "" || stuInfoReq.IdType == "" {
		log.Println("[Error] Empty jnuid or idtype.")
		return
	}
	SendSomeShitToJnu()

	// TODO: daemon化，每天定时打卡
	// for range time.Tick(24 * time.Hour) {
	// SendSomeShitToJnu()
	// }
}

// SendSomeShitToJnu 将你的打卡信息上传至jnu
func SendSomeShitToJnu() (err error) {
	var req *http.Request
	var resp *http.Response

	// ------------- stuinfo api -------------
	b, err := json.Marshal(stuInfoReq)
	if err != nil {
		log.Printf("[Marshal] failed, %s", err)
		return err
	}

	req, err = http.NewRequest(http.MethodPost, ApiStuInfo, bytes.NewReader(b))
	if err != nil {
		log.Printf("[NewRequest] failed.\nApi: %s\nErr: %s", ApiStuInfo, err)
		return err
	}

	req.Header.Set("Host", HeaderHost)
	req.Header.Set("Content-Type", HeaderContentType)
	req.Header.Set("User-Agent", HeaderUserAgent)

	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		log.Printf("[Do] failed, %s", err)
		return nil
	}

	stuInfoResp := new(models.StuInfoResp)
	if err = json.NewDecoder(resp.Body).Decode(stuInfoResp); err != nil {
		log.Printf("[JsonDecode] failed, %s", err)
		resp.Body.Close()
		return err
	}
	resp.Body.Close()

	log.Printf("[stuinfo] %s%s，%s", stuInfoResp.Data.JnuID, stuInfoResp.Data.Xm, stuInfoResp.Meta.Msg)

	// ------------- main api -------------
	mainReq := new(models.MainReq)

	mainReq.Jnuid = stuInfoReq.Jnuid
	mainReq.MainTable = stuInfoResp.Data.MainTable
	mainReq.SecondTable = stuInfoResp.Data.SecondTable

	mainReq.MainTable.ID = 0
	mainReq.MainTable.DeclareTime = time.Now().Format("2006-01-02")
	mainReq.MainTable.PersonName = stuInfoResp.Data.Xm
	mainReq.MainTable.Sex = stuInfoResp.Data.Xbm
	mainReq.MainTable.ProfessionName = stuInfoResp.Data.Zy
	mainReq.MainTable.CollegeName = stuInfoResp.Data.Yxsmc

	mainReq.SecondTable.ID = 0
	mainReq.SecondTable.MainID = 0

	b, err = json.Marshal(mainReq)
	if err != nil {
		log.Printf("[Marshal] failed, %s", err)
		return err
	}

	req, err = http.NewRequest(http.MethodPost, ApiMain, bytes.NewReader(b))
	if err != nil {
		log.Printf("[NewRequest] failed.\nApi: %s\nErr: %s", ApiMain, err)
		return err
	}

	req.Header.Set("Host", HeaderHost)
	req.Header.Set("Content-Type", HeaderContentType)
	req.Header.Set("User-Agent", HeaderUserAgent)

	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		log.Printf("[Do] failed, %s", err)
		return nil
	}

	mainResp := new(models.MainResp)
	if err = json.NewDecoder(resp.Body).Decode(mainResp); err != nil {
		resp.Body.Close()
		log.Printf("[JsonDecode] failed, %s", err)
		return err
	}
	resp.Body.Close()

	if !mainResp.Meta.Success {
		log.Printf("[main] %s", mainResp.Meta.Msg)
		return fmt.Errorf(mainResp.Meta.Msg)
	}
	log.Println("[main] Done.")
	return nil
}
