from pathlib import Path
from lxml import html as LH
from urllib.parse import quote
import re, json, html

ROOT=Path('.')
BASE='https://laixehodanang.me/'
def p(*texts): return ''.join('<p>'+t+'</p>' for t in texts)
def ul(*texts): return '<ul>'+''.join('<li>'+t+'</li>' for t in texts)+'</ul>'
def a(slug,label):return f'<a href="{slug}.html">{label}</a>'
def table(headers,rows):return '<table><thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'

# The reference theme's situation → explanation → practical steps → contact structure
# is adapted to static pages, retaining the existing URLs and business facts.
ARTICLES={
'lai-xe-ho-la-gi': {
 'title':'Lái xe hộ là gì? Cách hoạt động và khi nào nên sử dụng',
 'intro':'Bạn đi xe riêng đến buổi tiệc nhưng không muốn tự lái về? Dịch vụ lái xe hộ giúp bạn thuê người lái chính chiếc xe của mình đến nơi cần đến. Dưới đây là cách dịch vụ hoạt động và những điều nên biết trước khi đặt.',
 'desc':'Lái xe hộ là gì, khác taxi ở đâu và đặt tài xế thế nào? Tìm hiểu quy trình, chi phí và lưu ý khi giao ô tô, xe máy tại Đà Nẵng.',
 'tags':['Lái xe hộ','Ô tô','Xe máy'],
 'related':['huong-dan-dat-tai-xe-nhu-y-driver','lai-xe-ho-va-taxi','bang-gia-lai-xe-ho-da-nang'],
 'sections':[
 ('Lái xe hộ là gì?',p('Lái xe hộ là dịch vụ thuê tài xế điều khiển phương tiện của khách theo lộ trình đã thỏa thuận. Bạn bàn giao xe tại điểm hẹn; tài xế lái chiếc xe đó đưa bạn đến điểm trả. Khi hoàn tất, bạn nhận lại xe và chìa khóa.','Vì dùng xe của khách, dịch vụ này phù hợp khi bạn muốn cả người và xe cùng về nhà. Bạn cần nói rõ ô tô hay xe máy khi đặt, bởi cách bố trí chuyến và bảng giá của hai loại xe khác nhau.')),
 ('Khác gì với taxi và thuê xe có tài xế?',p('Với taxi hoặc thuê xe có tài xế, bên cung cấp dịch vụ bố trí cả phương tiện lẫn người lái. Với lái xe hộ, bạn đã có xe và chỉ cần người lái thay. Đây là điểm nên xác định trước khi so sánh giá.','Nếu không mang xe riêng, bạn có thể cân nhắc phương tiện đưa đón. Nếu xe đang ở bãi của nhà hàng và cần dùng vào sáng hôm sau, lái hộ giúp bạn giải quyết luôn việc đưa xe về. Xem thêm '+a('lai-xe-ho-va-taxi','so sánh lái xe hộ và taxi')+' để chọn theo tình huống của mình.')),
 ('Những lúc nào nên tìm người lái thay?',ul('<strong>Sau buổi tiệc:</strong> bạn không tự điều khiển xe khi đã uống rượu bia.','<strong>Khi mệt hoặc buồn ngủ:</strong> bạn muốn sắp xếp lại chuyến đi và nhờ người lái thay.','<strong>Lịch trình nhiều điểm:</strong> bạn cần người lái trong lúc đi họp, làm việc hoặc đưa đón người thân.','<strong>Chuyến đường dài:</strong> bạn muốn nghỉ ngơi trên xe và chủ động hỏi lịch tài xế trước ngày đi.')),
 ('Một chuyến lái xe hộ diễn ra như thế nào?',p('Ví dụ, bạn cần đưa ô tô từ nhà hàng về nhà sau buổi liên hoan. Khi liên hệ, hãy gửi địa chỉ nhà hàng, vị trí đỗ xe, điểm đến và giờ muốn về. Điều phối trao đổi giá, thời gian đón dự kiến và thông tin tài xế.','Tại điểm hẹn, bạn đối chiếu người nhận xe, kiểm tra tình trạng xe và giới thiệu thao tác riêng nếu có. Cuối chuyến, kiểm tra đồ dùng, nhận lại chìa khóa rồi thanh toán theo nội dung đã thống nhất. '+a('can-chuan-bi-gi-khi-ban-giao-xe','Danh sách chuẩn bị khi bàn giao xe')+' sẽ giúp bạn không bỏ sót những việc nhỏ này.')),
 ('Giá lái xe hộ tại Đà Nẵng được tính ra sao?',p('Chi phí phụ thuộc loại xe, quãng đường, thời điểm đi và yêu cầu chờ hoặc ghé thêm điểm. Bạn có thể xem '+a('bang-gia-lai-xe-ho-da-nang','bảng giá ô tô và xe máy')+' để dự trù, sau đó gửi hành trình để chốt giá trước chuyến.','Để đặt Như Ý Driver, gọi <a href="tel:0985666044">0985 666 044</a>, nhắn Zalo hoặc dùng biểu mẫu trên trang chủ. Nên liên hệ khi đã có giờ về dự kiến để chủ động sắp xếp.'))],
 'faq':[('Lái xe hộ có mang ô tô đến đón không?','Dịch vụ lái hộ sử dụng xe của bạn. Nếu cần cả xe đưa đón, hãy nói rõ nhu cầu khi liên hệ để chọn phương án phù hợp.'),('Có thể đặt tài xế lái xe máy không?','Bạn có thể gửi yêu cầu lái hộ xe máy, kèm loại xe, số người và địa chỉ đón để trao đổi cách bố trí chuyến.')]
},
'truong-hop-nen-goi-tai-xe-lai-ho':{
 'title':'7 trường hợp nên gọi tài xế lái hộ thay vì cố tự lái',
 'intro':'Không chỉ sau buổi tiệc, bạn còn có thể cần người lái thay khi mệt mỏi, đi xa hoặc có lịch trình dày. Nhận ra nhu cầu từ sớm giúp bạn chủ động đường về cho cả mình và chiếc xe.',
 'desc':'7 tình huống nên gọi tài xế lái hộ: sau tiệc, buồn ngủ, lịch nhiều điểm, đi tỉnh và đưa đón người thân. Cách chuẩn bị chuyến tại Đà Nẵng.',
 'tags':['Lái xe hộ','Sau tiệc','Theo giờ'],
 'related':['lai-xe-ho-sau-tiec-da-nang','thue-tai-xe-theo-gio-da-nang','huong-dan-dat-tai-xe-nhu-y-driver'],
 'sections':[
 ('1. Bạn đã uống rượu bia nhưng vẫn có xe ở điểm hẹn',p('Bạn đi ô tô hoặc xe máy đến buổi liên hoan và muốn mang xe về cùng? Hãy bố trí người lái thay từ trước khi rời bàn tiệc. Không nên dựa vào cảm giác “vẫn còn tỉnh” để quyết định tự lái.','Gửi địa chỉ quán và vị trí xe đang đỗ, sau đó chờ xác nhận giờ đón. Nếu cần hướng dẫn riêng cho phương tiện của mình, xem '+a('lai-xe-ho-sau-tiec-da-nang','dịch vụ lái hộ sau tiệc')+'.')),
 ('2. Buồn ngủ hoặc mệt sau một ngày dài',p('Một ca làm khuya hoặc hành trình dài có thể khiến bạn khó duy trì sự tập trung. Khi nhận thấy mình không đủ tỉnh táo, hãy tìm nơi dừng phù hợp rồi nhờ người hỗ trợ thay vì cố chạy cho hết đường.','Sau khi dừng, gửi vị trí, chiều di chuyển và một điểm mốc gần xe. Người đi cùng có thể giúp bạn liên hệ hoặc mô tả chỗ đỗ.')),
 ('3. Chưa quen đường hoặc chưa tự tin với chiếc xe',p('Đường đông, lối vào hầm hẹp hoặc một dòng xe chưa quen có thể khiến chuyến đi căng thẳng. Bạn có thể hỏi người lái thay cho đoạn hành trình cần hỗ trợ. Nhớ nêu dòng xe, số sàn hay số tự động và những thao tác riêng trên xe.')),
 ('4. Có nhiều cuộc hẹn trong cùng một buổi',p('Khi cần di chuyển qua văn phòng, ngân hàng hoặc nhiều điểm gặp khách, tài xế theo giờ giúp bạn tập trung vào lịch làm việc. Hãy tính cả khoảng chờ giữa các cuộc hẹn, không chỉ thời gian xe chạy. '+a('thue-tai-xe-theo-gio-da-nang','Thông tin thuê tài xế theo giờ')+' nêu những nội dung nên trao đổi trước.')),
 ('5. Muốn nghỉ ngơi trong chuyến đi tỉnh',p('Nếu dự định đi xa bằng xe riêng, bạn có thể gửi lịch trình để hỏi tài xế từ trước. Nêu ngày đi, điểm đến, một chiều hay khứ hồi, giờ về và các điểm dừng. Việc này giúp hai bên chuẩn bị thời gian di chuyển và nghỉ phù hợp.')),
 ('6. Cần đưa đón người thân bằng xe gia đình',p('Xe riêng có thể đã có sẵn ghế trẻ em, đồ dùng hoặc chỗ ngồi quen thuộc. Nếu bạn bận công việc và cần người lái thay, hãy báo rõ số người, địa điểm đón và người liên hệ ở mỗi đầu hành trình. Các hỗ trợ thêm cần được trao đổi trước.')),
 ('7. Muốn chủ động đường về sau sự kiện',p('Tiệc cưới, họp lớp hoặc sự kiện có giờ kết thúc dự kiến là những lúc bạn có thể sắp xếp người lái trước. Nếu có nhiều điểm trả khách, gửi đầy đủ địa chỉ ngay khi hỏi giá để tránh phải thay đổi lộ trình vào phút cuối.','Với Như Ý Driver, bạn có thể gọi <a href="tel:0985666044">0985 666 044</a> hoặc nhắn Zalo. Chuẩn bị điểm đón, điểm đến, loại xe và giờ đi để được tư vấn đúng nhu cầu.'))],
 'faq':[('Có cần đợi đến lúc ra về mới gọi không?','Bạn có thể liên hệ trước khi kết thúc buổi hẹn. Nếu chưa chắc giờ đi, hãy nêu khoảng thời gian dự kiến và báo lại khi có thay đổi.'),('Nên hỏi giá theo chuyến hay theo giờ?','Một lượt đi thường nên hỏi theo chuyến. Với nhiều điểm dừng và thời gian chờ, hãy gửi cả lịch trình để so sánh phương án theo giờ.')]
},
'can-chuan-bi-gi-khi-ban-giao-xe':{
 'title':'Cần chuẩn bị gì khi bàn giao xe cho tài xế lái hộ?',
 'intro':'Bàn giao xe không chỉ là đưa chìa khóa. Vài phút kiểm tra người nhận, tình trạng xe và điểm đến sẽ giúp chuyến đi rõ ràng hơn ngay từ lúc bắt đầu.',
 'desc':'Danh sách bàn giao ô tô, xe máy cho tài xế lái hộ: đối chiếu người nhận, kiểm tra xe, đồ dùng, lịch trình và việc cần làm khi nhận lại chìa khóa.',
 'tags':['Bàn giao xe','Ô tô','Xe máy'],
 'related':['huong-dan-dat-tai-xe-nhu-y-driver','lai-xe-ho-o-to-da-nang','lai-xe-ho-xe-may-da-nang'],
 'sections':[
 ('Gửi đúng chỗ xe đang đỗ',p('Địa chỉ nhà hàng hay toà nhà chưa chắc đã đủ để tìm thấy xe. Nếu xe ở hầm, hãy gửi tên cổng vào, tầng, số ô đỗ và vị trí thang máy gần nhất. Nếu đỗ ngoài đường, thêm một điểm mốc dễ nhận biết.','Chuẩn bị điện thoại còn pin để tài xế liên hệ khi tới. Bạn nên chờ ở vị trí đã thống nhất, tránh tự đổi điểm đón mà chưa báo lại.')),
 ('Đối chiếu thông tin trước khi giao chìa khóa',p('Kiểm tra tên hoặc thông tin nhận diện tài xế với người điều phối. Nếu có khác biệt, gọi lại đầu mối đặt chuyến trước khi bàn giao. Không giao xe chỉ vì một người nói rằng họ đến nhận chuyến.','Khi đi cùng nhóm, nên có một người phụ trách liên lạc và bàn giao. Điều này giúp tránh tình trạng người này giữ chìa khóa nhưng người khác lại trao đổi lịch trình.')),
 ('Cùng kiểm tra xe và những lưu ý vận hành',ul('Quan sát tình trạng bên ngoài xe và ghi nhận dấu vết sẵn có nếu cần.','Kiểm tra nhiên liệu hoặc mức pin; báo trước các đèn cảnh báo, trục trặc đã biết.','Giới thiệu cách khởi động, cần số, phanh tay, thẻ qua trạm hoặc thao tác khác với xe thông thường.','Chuẩn bị giấy tờ xe, chìa khóa, vé gửi xe và thẻ ra vào cần dùng.','Với xe máy, chuẩn bị mũ bảo hiểm và nói rõ xe số, tay ga hay côn tay.')),
 ('Thống nhất điểm đến và giữ đồ dùng cá nhân',p('Gửi địa chỉ cuối cùng, các điểm ghé và lối vào nơi trả xe. Nếu về chung cư hoặc khu có kiểm soát, nói rõ hầm được phép vào và người mở cổng. Bạn cũng nên hỏi cách tính khi chờ hoặc thay đổi điểm đến.','Cất điện thoại, ví, giấy tờ và đồ giá trị ở nơi mình quản lý được. Nếu xe có thiết bị hoặc vật dụng cần giữ nguyên vị trí, hãy nói trước với tài xế.')),
 ('Kiểm tra lại khi kết thúc chuyến',p('Trước khi xuống xe, nhìn lại ghế ngồi, cốp và các vị trí để đồ. Nhận chìa khóa, kiểm tra xe đã đỗ đúng nơi và hoàn tất thanh toán theo nội dung thống nhất. Nếu có điều gì cần làm rõ, trao đổi với tài xế và điều phối ngay khi bàn giao.','Bạn có thể lưu danh sách ngắn: <strong>đúng tài xế – đúng xe – rõ lộ trình – đủ đồ – nhận chìa khóa</strong>. Khi cần đặt chuyến mới, xem '+a('huong-dan-dat-tai-xe-nhu-y-driver','hướng dẫn đặt tài xế Như Ý Driver')+'.'))],
 'faq':[('Xe thuê tự lái có bàn giao cho tài xế dịch vụ được không?','Cần kiểm tra hợp đồng, sự đồng ý của bên cho thuê và điều kiện bảo hiểm trước. Không mặc định mọi xe thuê đều được phép đổi người lái.'),('Xe có thao tác đặc biệt thì nên báo lúc nào?','Nên báo từ khi đặt và hướng dẫn lại tại điểm bàn giao, trước lúc xe khởi hành.')]
},
'huong-dan-dat-tai-xe-nhu-y-driver':{
 'title':'Hướng dẫn đặt tài xế Như Ý Driver qua điện thoại và Zalo',
 'intro':'Chỉ cần chuẩn bị điểm đón, điểm đến, loại xe và giờ đi, bạn đã có thể gửi yêu cầu đặt tài xế Như Ý Driver. Chọn gọi điện, nhắn Zalo hoặc đặt trên website theo cách thuận tiện với mình.',
 'desc':'Cách đặt tài xế Như Ý Driver qua hotline 0985 666 044, Zalo hoặc website. Có mẫu tin nhắn, thông tin cần gửi và các bước xác nhận chuyến.',
 'tags':['Đặt tài xế','Zalo','Lái xe hộ'],
 'related':['bang-gia-lai-xe-ho-da-nang','can-chuan-bi-gi-khi-ban-giao-xe','dat-tai-xe-lai-ho-ban-dem-da-nang'],
 'sections':[
 ('Chuẩn bị 5 thông tin trước khi đặt',ul('<strong>Điểm đón:</strong> địa chỉ hoặc ghim vị trí, kèm chỗ xe đang đỗ.','<strong>Điểm đến:</strong> địa chỉ cuối cùng và các điểm cần ghé.','<strong>Loại xe:</strong> ô tô hay xe máy; thêm dòng xe và kiểu hộp số nếu là ô tô.','<strong>Giờ đi:</strong> thời gian cần đón và khoảng thời gian có thể thay đổi.','<strong>Liên hệ:</strong> tên, số điện thoại của người bàn giao xe.')),
 ('Cách 1: gọi hotline 0985 666 044',p('Gọi <a href="tel:0985666044">0985 666 044</a> khi muốn trao đổi trực tiếp về chuyến đi. Hãy nói ngắn gọn: bạn đang ở đâu, cần về đâu, đi xe gì và muốn khởi hành lúc nào. Nếu có nhiều điểm dừng hoặc cần chờ, báo ngay khi hỏi giá.','Sau khi trao đổi, kiểm tra lại tổng chi phí, giờ đón dự kiến và thông tin nhận xe. Việc liên hệ đặt chuyến và việc chuyến đã được xác nhận là hai bước khác nhau; bạn nên chờ phản hồi đầy đủ trước khi rời điểm hẹn.')),
 ('Cách 2: nhắn Zalo và gửi ghim vị trí',p('Mở <a href="https://zalo.me/0985666044">Zalo Như Ý Driver</a> để gửi thông tin bằng tin nhắn. Cách này thuận tiện khi cần chia sẻ vị trí, gửi mô tả bãi xe và xem lại nội dung đã thống nhất.','Bạn có thể dùng mẫu sau, rồi thay các phần trong ngoặc bằng thông tin thật:')+'<blockquote>Chào Như Ý Driver, mình cần lái hộ [ô tô/xe máy] lúc [giờ đi]. Đón tại [địa chỉ, vị trí đỗ xe], về [địa chỉ đến]. Có [số người] đi cùng, [điểm ghé nếu có]. Nhờ báo giá và thời gian đón giúp mình.</blockquote>',p('Nếu xe ở hầm hoặc địa điểm có nhiều cổng, gửi thêm tầng đỗ, cổng vào và ảnh mốc nhận biết khi cần.')),
 ('Cách 3: gửi yêu cầu trên website',p('Vào <a href="index.html#quick-booking">mục Đặt Tài Xế Nhanh</a> trên trang chủ. Chọn điểm đón, điểm đến, điền thông tin liên hệ và giờ đi. Ở phần ghi chú, nêu rõ loại xe cùng các yêu cầu riêng.','Giá hiển thị trên biểu mẫu là tạm tính. Điều phối sẽ trao đổi lại chi phí theo hành trình và loại phương tiện trước khi chốt chuyến. Với xe máy, bạn nên nói rõ loại xe để được tư vấn đúng bảng giá.')),
 ('Sau khi đặt: nhận xác nhận, gặp tài xế và bàn giao',p('Giữ điện thoại có thể liên lạc và chờ ở đúng điểm đã thống nhất. Khi tài xế đến, đối chiếu thông tin nhận diện rồi kiểm tra xe, chìa khóa và lộ trình. Đọc '+a('can-chuan-bi-gi-khi-ban-giao-xe','những việc cần chuẩn bị khi giao xe')+' nếu đây là lần đầu bạn sử dụng.','Nếu đổi giờ, đổi điểm đón hoặc không còn nhu cầu, báo sớm qua đúng kênh đã đặt. Hãy nêu rõ thông tin mới để tránh nhầm với lịch cũ.'))],
 'faq':[('Có cần tải ứng dụng riêng không?','Bạn có thể đặt qua hotline, Zalo hoặc biểu mẫu trên website; không cần tải thêm ứng dụng để dùng các kênh này.'),('Chưa biết chính xác giờ về thì đặt được không?','Bạn có thể hỏi trước với khoảng giờ dự kiến, sau đó thống nhất cách báo lại giờ đi. Khả năng bố trí tài xế được kiểm tra theo lịch thực tế.')]
},
'dat-tai-xe-lai-ho-ban-dem-da-nang':{
 'title':'Đặt tài xế lái hộ ban đêm tại Đà Nẵng: kinh nghiệm cần biết',
 'intro':'Ra về muộn sau tiệc hoặc một ngày làm việc dài, bạn thường muốn chuyến đi gọn gàng và ít phải chờ. Chuẩn bị giờ đón, vị trí xe và chi phí từ trước sẽ giúp việc đặt tài xế ban đêm thuận tiện hơn.',
 'desc':'Kinh nghiệm đặt tài xế lái hộ ban đêm tại Đà Nẵng: chọn điểm đón, báo giờ về, xem phụ phí sau 23h và bàn giao xe. Hotline 0985 666 044.',
 'tags':['Ban đêm','Sau tiệc','Đặt tài xế'],
 'related':['lai-xe-ho-sau-tiec-da-nang','bang-gia-lai-xe-ho-da-nang','huong-dan-dat-tai-xe-nhu-y-driver'],
 'sections':[
 ('Liên hệ từ khi đã có giờ về dự kiến',p('Nếu biết buổi hẹn kết thúc vào khoảng nào, hãy gửi yêu cầu trước lúc ra bãi xe. Bạn sẽ có thời gian trao đổi giá và chờ thông tin tài xế ở ngay địa điểm đang ngồi. Nếu lịch còn thay đổi, báo khoảng giờ dự kiến thay vì chốt một giờ mình chưa chắc.','Với buổi tiệc nhiều người hoặc có điểm dừng dọc đường, gửi luôn các địa chỉ cần trả khách. Điều phối cần biết toàn bộ hành trình để tư vấn lịch và chi phí phù hợp.')),
 ('Điểm đón ban đêm cần dễ tìm và dễ liên lạc',p('Chọn chỗ có ánh sáng và cho phép dừng, đỗ. Gửi ghim vị trí kèm tên nhà hàng, số cổng hoặc tầng hầm; không chỉ gửi một địa chỉ chung nếu xe nằm sâu trong bãi. Khi tài xế gọi, mô tả mốc gần xe để hai bên gặp nhau thuận tiện.','Giữ điện thoại còn pin và bật chuông. Nếu bạn đi cùng nhóm, thống nhất một người phụ trách liên hệ để tránh nhiều vị trí đón được gửi cùng lúc.')),
 ('Phụ phí giờ khuya được tính thế nào?',p('Bảng giá ô tô của Như Ý Driver có phụ phí <strong>50.000đ cho khung 23:00–05:59</strong>. Hãy báo giờ khởi hành dự kiến khi hỏi giá, nhất là khi buổi tiệc có thể kéo dài qua 23 giờ.','Bạn có thể xem '+a('bang-gia-lai-xe-ho-da-nang','bảng giá lái xe hộ')+' để dự trù chi phí. Thời gian chờ, các điểm ghé và khoản liên quan đến hành trình cần được trao đổi trước; tổng giá thực tế được xác nhận trước chuyến đi.')),
 ('Gặp đúng tài xế rồi mới giao xe',p('Đối chiếu thông tin tài xế với điều phối và báo các thao tác riêng của xe. Nếu xe ở hầm có thẻ ra vào, chuẩn bị thẻ trước khi khởi hành. Với xe máy, cần trao đổi cả việc bố trí người đi cùng và chuẩn bị mũ bảo hiểm.','Tại điểm đến, thông báo trước lối vào nhà, hầm hoặc nơi được phép đỗ. Nhận lại chìa khóa và kiểm tra đồ dùng trước khi kết thúc chuyến.')),
 ('Nếu thay đổi giờ về thì xử lý ra sao?',p('Nhắn hoặc gọi lại ngay khi biết lịch mới. Ghi rõ bạn đổi giờ đón, đổi địa chỉ hay muốn thêm điểm dừng; điều phối sẽ kiểm tra khả năng sắp xếp lại. Đừng tự di chuyển sang điểm khác trong lúc tài xế đang tìm xe ở vị trí cũ.','Để đặt Như Ý Driver ban đêm tại Đà Nẵng, gọi <a href="tel:0985666044">0985 666 044</a> hoặc gửi Zalo cùng ghim vị trí. Xem '+a('huong-dan-dat-tai-xe-nhu-y-driver','hướng dẫn đặt tài xế')+' để chuẩn bị đủ thông tin.'))],
 'faq':[('Ban đêm có chắc tài xế đến ngay không?','Thời gian đón phụ thuộc vị trí, giao thông và lịch tài xế. Bạn sẽ được trao đổi thời gian dự kiến khi xác nhận yêu cầu.'),('Xe máy có dùng bảng giá ô tô không?','Không. Xe máy có biểu phí riêng; hãy báo đúng loại xe khi đặt.')]
},
'buon-ngu-khi-lai-xe':{
 'title':'Buồn ngủ khi lái xe: dừng thế nào và sắp xếp đường về ra sao?',
 'intro':'Đường về còn một đoạn nhưng bạn đã khó giữ sự tập trung? Lúc này, điều cần làm là tìm phương án dừng và nghỉ phù hợp, thay vì cố hoàn thành chuyến đi bằng mọi giá.',
 'desc':'Khi buồn ngủ trên đường, ưu tiên dừng ở nơi phù hợp, nhờ người hỗ trợ và sắp xếp người lái thay. Các thông tin cần gửi khi gọi tài xế tại Đà Nẵng.',
 'tags':['Lái xe hộ','Ban đêm','Ô tô'],
 'related':['lai-xe-ho-o-to-da-nang','dat-tai-xe-lai-ho-ban-dem-da-nang','can-chuan-bi-gi-khi-ban-giao-xe'],
 'sections':[
 ('Đừng lấy quãng đường còn lại làm lý do cố lái',p('Sau ca làm muộn, một buổi họp dài hoặc chuyến đi xa, bạn có thể chỉ muốn về đến nhà thật nhanh. Nhưng khi đã nhận thấy mình khó tập trung, việc cố chạy thêm một đoạn không giải quyết được tình trạng đó.','Nếu có người đi cùng, hãy nói rõ rằng bạn cần dừng và nhờ họ hỗ trợ tìm vị trí phù hợp. Tránh vừa lái vừa dùng điện thoại để tìm dịch vụ hoặc nhắn vị trí.')),
 ('Ưu tiên đưa xe đến vị trí dừng phù hợp',p('Quan sát đường và biển báo để tìm nơi được phép dừng, đỗ, chẳng hạn bãi xe hoặc điểm dừng phù hợp với tuyến đang đi. Không phanh dừng đột ngột ở vị trí cản trở dòng xe. Tình huống và điều kiện đường thực tế cần được đặt lên trước kế hoạch đến nơi.','Chỉ sau khi xe đã dừng phù hợp, bạn mới nên liên hệ người thân, người đi cùng hoặc dịch vụ hỗ trợ. Nếu không thể tiếp tục hành trình, hãy sắp xếp lại việc về nhà thay vì giữ nguyên kế hoạch cũ.')),
 ('Chọn người lái thay hoặc phương tiện khác',p('Bạn có thể nhờ một người đủ điều kiện lái thay, gọi tài xế lái hộ cho xe riêng hoặc bố trí gửi xe tại nơi cho phép rồi đi phương tiện khác. Lựa chọn phụ thuộc vị trí đang dừng, người có thể hỗ trợ và việc bạn có cần mang xe về ngay không.','Nếu chọn dịch vụ lái hộ, xem '+a('lai-xe-ho-o-to-da-nang','thông tin lái hộ ô tô tại Đà Nẵng')+'. Bạn cần chờ điều phối xác nhận tài xế và giờ đón, không tự chạy tiếp chỉ để rút ngắn khoảng cách gặp.')),
 ('Thông tin giúp người hỗ trợ tìm đúng xe',ul('Tên đường, chiều di chuyển và điểm mốc gần nơi dừng.','Ghim vị trí, tên bãi xe hoặc khu vực được phép đỗ.','Dòng xe, số sàn hay số tự động và biển số khi cần nhận diện.','Số người đi cùng, điểm đến và người liên lạc.','Lưu ý về lối vào bãi, thẻ xe hoặc thời gian địa điểm đóng cửa.')),
 ('Chủ động hơn cho những chuyến đi sau',p('Nếu dự kiến làm việc muộn hoặc di chuyển nhiều giờ, nên cân nhắc thời gian nghỉ và người lái thay từ trước khi lên đường. Với lịch trình đi tỉnh, gửi kế hoạch sớm để trao đổi thời gian chạy, điểm dừng và lượt về.','Trước lúc giao xe, đối chiếu người nhận và báo tình trạng phương tiện. '+a('can-chuan-bi-gi-khi-ban-giao-xe','Danh sách bàn giao xe')+' giúp bạn chuẩn bị gọn ngay cả khi đang mệt.'))],
 'faq':[('Có nên vừa chạy vừa gọi tài xế đến gặp không?','Hãy ưu tiên dừng ở vị trí phù hợp rồi mới liên hệ. Sau đó thống nhất một điểm gặp rõ ràng và báo lại nếu buộc phải thay đổi chỗ đỗ.'),('Có thể để xe lại và đi phương tiện khác không?','Bạn cần hỏi địa điểm về quyền gửi xe, giờ lấy xe và chi phí trước khi lựa chọn phương án này.')]
},
'uong-ruou-bia-mang-theo-xe-may':{
 'title':'Uống rượu bia nhưng mang theo xe máy: đưa cả người và xe về thế nào?',
 'intro':'Đi xe máy đến buổi tiệc rồi mới nghĩ đến đường về là tình huống nhiều người gặp phải. Bạn có thể cân nhắc lái hộ xe máy hoặc gửi xe lại, tùy việc cần mang xe về ngay và tình trạng của người đi cùng.',
 'desc':'Mang theo xe máy khi đi tiệc: chọn lái hộ hay gửi xe lại? Cách đặt tài xế, chuẩn bị mũ bảo hiểm và hỏi giá xe máy tại Đà Nẵng.',
 'tags':['Xe máy','Sau tiệc','Đặt tài xế'],
 'related':['lai-xe-ho-xe-may-da-nang','bang-gia-lai-xe-ho-da-nang','lai-xe-ho-va-taxi'],
 'sections':[
 ('Trước hết, bỏ phương án tự lái sau buổi tiệc',p('Việc chiếc xe đang ở ngay bãi không có nghĩa bạn phải tự điều khiển để mang nó về. Hãy tách hai việc: bạn sẽ về bằng cách nào và xe sẽ được xử lý ra sao. Từ đó, chọn phương án phù hợp thay vì quyết định chỉ vì ngại quay lại lấy xe.','Nếu có bạn bè hoặc người thân đi cùng, trao đổi trước ai sẽ liên hệ và giữ chìa khóa. Bạn nên xử lý việc đặt xe khi còn ở trong quán, không đợi đến lúc đứng ngoài bãi mới tìm phương án.')),
 ('Phương án 1: gửi yêu cầu lái hộ xe máy',p('Dịch vụ '+a('lai-xe-ho-xe-may-da-nang','lái hộ xe máy tại Đà Nẵng')+' dành cho nhu cầu có xe riêng và cần người điều khiển thay. Khi liên hệ, nêu xe tay ga, xe số hay côn tay, số người cần về và địa chỉ trả. Cách bố trí người và xe cần được thống nhất trước.','Nếu người đi cùng không thể ngồi vững trên xe, hãy nhờ người thân hỗ trợ và trao đổi phương tiện khác phù hợp hơn. Không chỉ chốt việc đưa xe về mà bỏ qua nhu cầu di chuyển của người.')),
 ('Phương án 2: gửi xe lại rồi quay lại lấy',p('Nếu địa điểm cho phép giữ xe qua đêm, bạn có thể chọn phương tiện khác để về. Hỏi trước giờ đóng bãi, phí gửi, vé nhận xe và giờ được lấy vào hôm sau. Không mặc định quán nào cũng giữ xe qua đêm.','Khi tính chi phí, cộng cả lượt về nhà, phí gửi và lượt quay lại lấy xe. Nếu sáng hôm sau cần xe sớm, hãy xem giờ mở bãi có khớp kế hoạch của mình không.')),
 ('Chuẩn bị gì khi đặt lái hộ xe máy?',ul('Gửi ghim vị trí cùng tên bãi hoặc cổng nhận xe.','Chuẩn bị chìa khóa, vé xe và mũ bảo hiểm phù hợp.','Nêu rõ số người cần di chuyển, không chỉ loại xe.','Hỏi đúng giá xe máy, giờ đi và các điểm ghé.','Đối chiếu tài xế trước khi bàn giao chìa khóa.')),
 ('Giá xe máy khác giá ô tô',p('Như Ý Driver có '+a('bang-gia-lai-xe-ho-da-nang','bảng giá riêng cho xe máy và ô tô')+'. Hãy chọn đúng loại phương tiện khi xem giá tham khảo và xác nhận tổng phí cho hành trình của mình. Nếu về khuya, hỏi thêm phụ phí theo giờ đi.','Gọi <a href="tel:0985666044">0985 666 044</a> hoặc nhắn Zalo với địa chỉ đón, điểm đến và loại xe. Sau khi được xác nhận, chờ ở điểm hẹn đã thống nhất để việc nhận xe thuận tiện.'))],
 'faq':[('Đi hai người và có một xe máy thì cần báo gì?','Báo đầy đủ số người cần về để điều phối trao đổi cách bố trí. Không tự mặc định một phương án chở người sẽ phù hợp cho mọi trường hợp.'),('Chỉ cần đưa xe về, không đi cùng thì sao?','Hãy nêu rõ yêu cầu khi liên hệ để thống nhất người bàn giao, người nhận xe và điều kiện thực hiện trước khi đặt.')]
},
'di-tiec-bang-o-to-da-nang':{
 'title':'Đi tiệc bằng ô tô tại Đà Nẵng: chuẩn bị đường về từ trước',
 'intro':'Mang ô tô đi tiệc giúp bạn chủ động lúc đến, nhưng đường về cũng cần một kế hoạch riêng. Nếu dự định uống rượu bia hoặc không muốn tự lái, hãy sắp xếp người lái thay hay chỗ gửi xe từ trước.',
 'desc':'Đi tiệc bằng ô tô ở Đà Nẵng: cách chọn lái xe hộ, gửi xe hoặc phương tiện đưa đón; chuẩn bị chỗ đỗ, giờ về và các điểm trả khách.',
 'tags':['Ô tô','Sau tiệc','Ban đêm'],
 'related':['lai-xe-ho-sau-tiec-da-nang','lai-xe-ho-va-taxi','dat-tai-xe-lai-ho-ban-dem-da-nang'],
 'sections':[
 ('Lên phương án trước khi vào tiệc',p('Khi đến nhà hàng hoặc địa điểm sự kiện, ghi lại nơi đỗ và hỏi giờ đóng bãi. Nếu bạn đã dự định không tự lái về, trao đổi với người đi cùng về phương án cuối buổi: ai liên hệ, cả nhóm về cùng hay chia điểm trả.','Chủ động từ đầu giúp bạn tránh cảnh buổi tiệc kết thúc mới đi tìm người giữ chìa khóa, hỏi lại địa chỉ và quyết định có để xe qua đêm được không.')),
 ('Muốn cả người và ô tô về cùng: hỏi tài xế lái hộ',p('Với '+a('lai-xe-ho-sau-tiec-da-nang','dịch vụ lái xe hộ sau tiệc')+', tài xế đến điểm hẹn và lái chính ô tô của bạn. Bạn không phải sắp xếp thêm một lượt quay lại lấy xe nếu chuyến được xác nhận và thực hiện theo kế hoạch.','Gửi dòng xe, hộp số, vị trí đỗ, điểm đến và giờ muốn về. Nếu nhà hàng có hầm hoặc nhiều cổng, thêm tầng đỗ và lối vào. Tại điểm hẹn, đối chiếu thông tin tài xế trước khi giao xe.')),
 ('Có thể gửi ô tô lại: cân nhắc phương tiện đưa đón',p('Nếu chưa cần dùng ô tô vào sáng hôm sau và địa điểm cho phép giữ xe, bạn có thể gửi xe rồi đặt phương tiện khác. Hỏi rõ phí, giờ lấy xe và người phụ trách bãi. Giữ vé xe ở nơi dễ tìm.','Để so sánh chi phí, tính cả lượt quay lại lấy ô tô. Bài '+a('lai-xe-ho-va-taxi','lái xe hộ và taxi nên chọn dịch vụ nào')+' giúp bạn nhìn đủ nhu cầu, thay vì chỉ so giá một lượt về.')),
 ('Đi theo nhóm: gửi đủ các điểm trả khách',p('Khi nhiều người về chung ô tô, thống nhất thứ tự các điểm xuống và số chỗ phù hợp. Gửi các địa chỉ ngay lúc hỏi giá, đặc biệt khi có điểm nằm xa lộ trình chính hoặc cần vào hẻm.','Nếu thay đổi trong buổi tiệc, báo lại trước khi xe khởi hành. Việc thêm chặng hoặc kéo dài thời gian có thể làm thay đổi chi phí và lịch của tài xế.')),
 ('Chốt chuyến và chuẩn bị khi về nhà',ul('Kiểm tra tổng giá, giờ đón dự kiến và thông tin người nhận xe.','Giữ điện thoại có thể liên lạc, chuẩn bị chìa khóa và vé bãi.','Báo lối vào nhà, hầm chung cư hoặc chỗ đỗ tại điểm trả.','Nhận lại chìa khóa và kiểm tra đồ cá nhân trước khi kết thúc chuyến.')+p('Nếu cần đặt tài xế tại Đà Nẵng, liên hệ Như Ý Driver qua <a href="tel:0985666044">0985 666 044</a> hoặc Zalo. Bạn có thể xem '+a('bang-gia-lai-xe-ho-da-nang','bảng giá ô tô')+' trước để dự trù.'))],
 'faq':[('Nên báo giờ đón thế nào nếu tiệc chưa kết thúc?','Hãy nêu khoảng giờ dự kiến và hỏi cách báo lại giờ chính thức. Khi kế hoạch thay đổi, liên hệ sớm để kiểm tra lịch mới.'),('Có cần báo xe số sàn hay số tự động không?','Có. Thông tin dòng xe và hộp số giúp điều phối trao đổi người lái phù hợp với yêu cầu của bạn.')]
},
'thue-tai-xe-theo-gio-hay-theo-ngay':{
 'title':'Thuê tài xế theo giờ hay theo ngày: chọn theo lịch trình nào?',
 'intro':'Một buổi có hai cuộc hẹn sẽ khác chuyến công tác kéo dài từ sáng đến tối. Muốn chọn cách thuê tài xế phù hợp, hãy so sánh cả thời gian chờ, số chặng và tổng chi phí thay vì chỉ nhìn đơn giá.',
 'desc':'So sánh thuê tài xế theo giờ và theo ngày: lịch trình phù hợp, thời gian chờ, khoản ngoài gói và cách yêu cầu báo giá tại Đà Nẵng.',
 'tags':['Theo giờ','Theo ngày','Ô tô'],
 'related':['thue-tai-xe-theo-gio-da-nang','thue-tai-xe-theo-ngay-da-nang','thue-tai-xe-di-tinh-da-nang'],
 'sections':[
 ('Theo giờ và theo ngày khác nhau ở đâu?',p('Thuê theo giờ thường bắt đầu từ một khoảng thời gian sử dụng cụ thể. Thuê theo ngày thường được trao đổi cho lịch trình dài hơn với nhiều chặng trong cùng ngày. Tuy nhiên, tên gói chưa nói hết số giờ, phạm vi và các khoản đã bao gồm.','Điểm cần xem là bạn được dùng tài xế từ lúc nào đến lúc nào, thời gian chờ tính ra sao và nếu về muộn thì phí thay đổi thế nào. Một gói gọi là “theo ngày” cũng cần được mô tả bằng điều kiện cụ thể.')),
 ('Khi nào nên hỏi phương án theo giờ?',p('Bạn có hai cuộc hẹn trong buổi chiều, cần ghé ngân hàng rồi tới văn phòng và kết thúc trước tối. Trong tình huống này, bạn có thể gửi giờ bắt đầu, giờ xong và các địa chỉ để hỏi '+a('thue-tai-xe-theo-gio-da-nang','giá thuê tài xế theo giờ')+'.','Hãy tính cả thời gian tài xế chờ trong lúc bạn làm việc. Nếu chỉ cần một lượt đưa xe từ điểm A tới B, nên hỏi thêm giá theo chuyến để so sánh trên cùng nhu cầu.')),
 ('Khi nào nên hỏi phương án theo ngày?',p('Với lịch công tác từ sáng tới chiều, đưa đón nhiều cuộc hẹn hoặc hành trình có nhiều khoảng chờ, bạn nên gửi cả kế hoạch để hỏi '+a('thue-tai-xe-theo-ngay-da-nang','phương án thuê tài xế theo ngày')+'.','Nêu giờ xuất phát, giờ kết thúc dự kiến, các điểm ghé và khả năng thay đổi lịch. Điều phối cần kiểm tra lịch tài xế và báo phạm vi phục vụ trước khi bạn chốt. Nếu đi tỉnh hoặc ở lại qua đêm, hãy nói rõ ngay từ đầu.')),
 ('Bảng so sánh những điều cần hỏi',table(['Nội dung','Theo giờ','Theo ngày'],[
 ('Lịch phù hợp','Khoảng thời gian ngắn, giờ bắt đầu và kết thúc khá rõ','Lịch dài, nhiều chặng hoặc nhiều khoảng chờ'),('Thời lượng','Hỏi số giờ tối thiểu và cách làm tròn','Hỏi số giờ bao gồm trong ngày'),('Khi kéo dài','Hỏi phí vượt giờ','Hỏi giờ kết thúc gói và phí ngoài gói'),('Các khoản khác','Chờ, đỗ xe, cầu đường theo thỏa thuận','Chờ, quãng đường, đỗ xe, cầu đường và ăn nghỉ nếu có') ])),
 ('Cách lấy báo giá dễ so sánh',p('Gửi cùng một lịch trình cho cả hai phương án. Ví dụ: đón lúc nào, ghé đâu, mỗi điểm dự kiến chờ bao lâu và kết thúc ở địa chỉ nào. Hỏi tổng phí dự kiến, thời lượng bao gồm và cách tính khi phát sinh.','Bạn có thể nhắn Như Ý Driver qua Zalo hoặc gọi <a href="tel:0985666044">0985 666 044</a>. Chọn phương án có phạm vi khớp lịch trình, không chỉ chọn con số đơn giá thấp hơn.'))],
 'faq':[('Thuê theo ngày có nghĩa là dùng đủ 24 giờ không?','Không nên hiểu mặc định như vậy. Bạn cần hỏi số giờ phục vụ, thời điểm bắt đầu và kết thúc được bao gồm trong báo giá.'),('Đổi từ lịch nội thành sang đi tỉnh có cần báo không?','Có. Thay đổi tuyến có thể ảnh hưởng thời gian, chi phí và việc bố trí tài xế; cần thống nhất lại trước khi đi.')]
},
'thue-xe-tu-lai-goi-tai-xe':{
 'title':'Thuê xe tự lái có thể gọi tài xế lái thay không?',
 'intro':'Đang thuê ô tô nhưng có buổi tiệc hoặc lịch đi xa khiến bạn muốn nhờ người lái thay? Trước khi giao chìa khóa, hãy kiểm tra điều khoản thuê xe và hỏi bên cho thuê về việc bổ sung người lái.',
 'desc':'Xe thuê tự lái có được giao cho tài xế lái hộ? Những điều cần hỏi bên cho thuê, giấy tờ người lái và điều kiện bảo hiểm trước khi đặt dịch vụ.',
 'tags':['Xe thuê tự lái','Ô tô','Bàn giao xe'],
 'related':['lai-xe-ho-o-to-da-nang','can-chuan-bi-gi-khi-ban-giao-xe','huong-dan-dat-tai-xe-nhu-y-driver'],
 'sections':[
 ('Không mặc định xe thuê được giao cho bất kỳ người lái nào',p('Xe đang nằm trong thời gian thuê không có nghĩa bạn tự do giao lại cho một người khác điều khiển. Điều kiện về người lái có thể được quy định ngay trong hợp đồng hoặc thỏa thuận với bên cho thuê.','Bạn nên kiểm tra trước khi đặt tài xế, thay vì chốt chuyến rồi mới hỏi quyền sử dụng xe. Việc này giúp tránh thay đổi kế hoạch vào sát giờ khởi hành.')),
 ('Đọc phần người lái và phạm vi sử dụng xe',ul('Hợp đồng ghi tên người được điều khiển xe như thế nào?','Có được bổ sung người lái trong thời gian thuê không?','Bên cho thuê yêu cầu giấy tờ hoặc xác nhận gì khi thêm người?','Lịch trình có thay đổi phạm vi sử dụng hoặc thời gian trả xe không?','Trách nhiệm khi bàn giao cho người khác được thỏa thuận ra sao?')),
 ('Hỏi trực tiếp bên cho thuê và kiểm tra bảo hiểm',p('Bạn có thể hỏi: “Tôi muốn nhờ tài xế dịch vụ lái xe trong khoảng thời gian này. Hợp đồng có cho phép không, cần gửi giấy tờ nào và có phải bổ sung thỏa thuận không?” Nêu đầy đủ mục đích, thời gian và tuyến đi để nhận phản hồi đúng tình huống.','Đồng thời hỏi về điều kiện bảo hiểm liên quan đến người điều khiển. Không suy đoán rằng đổi người lái vẫn giữ nguyên mọi điều kiện áp dụng. Lưu lại phản hồi của bên cho thuê và đối chiếu cùng hợp đồng.')),
 ('Được đồng ý rồi mới gửi yêu cầu tài xế',p('Khi liên hệ '+a('lai-xe-ho-o-to-da-nang','dịch vụ lái hộ ô tô')+', nói rõ đây là xe thuê. Gửi dòng xe, hộp số, thời gian cần người lái và những điều kiện bên cho thuê đã đưa ra. Nếu cần giấy tờ để bổ sung người lái, trao đổi sớm thay vì đợi đến điểm nhận xe.','Trước lúc đi, kiểm tra tình trạng phương tiện và những lưu ý vận hành cùng tài xế. Bạn có thể dùng '+a('can-chuan-bi-gi-khi-ban-giao-xe','danh sách bàn giao xe')+' để ghi lại các việc cần làm.')),
 ('Nếu chưa được xác nhận thì chọn phương án nào?',p('Khi điều khoản còn chưa rõ hoặc bên cho thuê không đồng ý, hãy hoãn việc giao xe cho người khác. Bạn có thể hỏi chỗ gửi xe và dùng phương tiện đưa đón cho chuyến đi của mình, sau đó sắp xếp lại việc nhận hoặc trả xe với bên cho thuê.','Để được tư vấn yêu cầu lái thay, liên hệ Như Ý Driver qua <a href="tel:0985666044">0985 666 044</a> hoặc Zalo. Việc bố trí tài xế chỉ nên tiến hành sau khi các điều kiện sử dụng chiếc xe đã rõ ràng.'))],
 'faq':[('Tài xế có bằng lái thì đã đủ điều kiện nhận xe thuê chưa?','Ngoài điều kiện của người lái, vẫn phải kiểm tra thỏa thuận với bên cho thuê và điều kiện bảo hiểm liên quan đến chiếc xe.'),('Chỉ nhờ lái một đoạn ngắn có cần hỏi chủ xe không?','Bạn vẫn nên kiểm tra điều khoản và hỏi bên cho thuê trước khi đổi người điều khiển, dù quãng đường ngắn.')]
},
'lai-xe-ho-va-taxi':{
 'title':'Lái xe hộ và taxi: chọn cách nào khi đi tiệc bằng xe riêng?',
 'intro':'Cùng là nhu cầu về nhà sau buổi hẹn, nhưng có xe riêng đi cùng hay không sẽ làm lựa chọn khác nhau. So sánh đúng nhu cầu giúp bạn tính được cả chi phí đi lại lẫn việc đưa xe về.',
 'desc':'So sánh lái xe hộ và taxi khi đi tiệc tại Đà Nẵng: phương tiện, việc đưa xe riêng về, chi phí gửi xe, lượt lấy xe và thông tin nên hỏi trước.',
 'tags':['Lái xe hộ','Taxi','Sau tiệc'],
 'related':['lai-xe-ho-la-gi','lai-xe-ho-sau-tiec-da-nang','bang-gia-lai-xe-ho-da-nang'],
 'sections':[
 ('Điểm khác nhau nằm ở chiếc xe sử dụng',p('Taxi bố trí xe để đưa đón bạn. Lái xe hộ bố trí người điều khiển chính xe bạn đang sử dụng. Vì vậy, nếu bạn đến buổi tiệc bằng ô tô hoặc xe máy riêng, lái hộ có thể giải quyết cả việc đưa người và xe về cùng.','Nếu không mang theo xe, bạn thường chỉ cần một phương tiện đưa đón. Khi đó, nên lựa chọn theo số người, điểm đón và nhu cầu di chuyển thay vì tìm người lái cho một chiếc xe không có ở điểm hẹn.')),
 ('So sánh theo cùng một hành trình',table(['Điều cần xem','Lái xe hộ','Taxi'],[
 ('Phương tiện','Xe của khách','Xe được đặt để đưa đón'),('Xe riêng ở điểm hẹn','Có thể đưa về cùng theo chuyến đã thống nhất','Cần phương án gửi xe hoặc lấy lại sau'),('Thông tin phải báo','Loại xe, vị trí xe, hành trình và giờ đi','Điểm đón, điểm đến, số người và nhu cầu xe'),('Chi phí nên tính','Giá lái hộ, chờ và các khoản của hành trình','Giá lượt đi, gửi xe và lượt lấy xe riêng nếu có'),('Thời gian đón','Kiểm tra lịch tài xế thực tế','Kiểm tra khả năng nhận chuyến thực tế') ])),
 ('Khi nào nên cân nhắc lái xe hộ?',p('Bạn cần dùng xe riêng vào sáng sớm, nhà hàng không giữ xe qua đêm hoặc không muốn quay lại lấy xe vào hôm sau. Khi đó, hãy hỏi '+a('lai-xe-ho-sau-tiec-da-nang','dịch vụ lái xe hộ sau tiệc')+' với đầy đủ loại xe, điểm đến và giờ đón.','Với nhóm đi cùng xe gia đình, bạn cũng nên báo số người, các điểm trả và vị trí đỗ ở nhà. Những chi tiết này giúp báo giá phản ánh đúng hành trình thay vì chỉ một quãng đường ước chừng.')),
 ('Khi nào phương tiện đưa đón có thể phù hợp hơn?',p('Nếu không mang xe hoặc có nơi gửi xe phù hợp và chưa cần dùng ngay, bạn có thể cân nhắc taxi hay phương tiện đưa đón khác. Trước khi để xe lại, hỏi giờ đóng bãi, giờ nhận lại và phí giữ.','Đừng chỉ tính giá lượt về. Nếu phải đi thêm một lượt để lấy xe vào hôm sau, hãy cộng khoản đó cùng phí bãi rồi mới so với giá lái hộ. Không có một phương án luôn rẻ hơn hoặc nhanh hơn trong mọi tình huống.')),
 ('Ba câu hỏi giúp chốt lựa chọn',ul('Tôi có cần đưa xe riêng về ngay tối nay không?','Nếu gửi lại, tôi có chỗ gửi được phép và thời gian lấy xe thuận tiện không?','Tổng chi phí, thời gian đón và các điểm dừng của mỗi phương án là gì?')+p('Nếu chọn lái hộ, xem '+a('bang-gia-lai-xe-ho-da-nang','bảng giá ô tô và xe máy Như Ý Driver')+' rồi gửi hành trình để chốt phí. Hotline/Zalo: <a href="tel:0985666044">0985 666 044</a>.'))],
 'faq':[('Lái hộ có luôn rẻ hơn taxi không?','Không nên kết luận chung. Hãy so cùng hành trình và tính cả việc gửi, lấy lại xe riêng nếu bạn chọn taxi.'),('Chọn lái hộ thì có cần nói rõ xe máy hay ô tô không?','Có. Loại xe ảnh hưởng cách bố trí chuyến và mức phí, nên cần báo ngay khi đặt.')]
}
}

def faq(entries):
 return ''.join('<details><summary>'+q+'</summary><p>'+answer+'</p></details>' for q,answer in entries)

def tags_html(tags):
 return '<nav class="topic-tags" aria-label="Chủ đề bài viết"><span>Chủ đề:</span>'+''.join(f'<a href="tin-tuc.html?chu-de={quote(tag)}#noi-dung">#{html.escape(tag)}</a>' for tag in tags)+'</nav>'

for slug,data in ARTICLES.items():
 file=ROOT/(slug+'.html');source=file.read_text(encoding='utf-8')
 source=re.sub(r'<script type="application/ld\+json">(.*?)</script>',lambda m:'' if json.loads(m.group(1)).get('@type')=='Article' else m.group(),source,flags=re.S)
 doc=LH.fromstring(source)
 oldtitle=doc.xpath('//h1')[0].text_content()
 # Update text title occurrences in head, breadcrumb and breadcrumb schema consistently.
 source=source.replace(oldtitle,data['title'])
 source=re.sub(r'(<meta name="description" content=")[^"]*',lambda m:m.group(1)+html.escape(data['desc'],quote=True),source)
 source=re.sub(r'(<meta property="og:description" content=")[^"]*',lambda m:m.group(1)+html.escape(data['desc'],quote=True),source)
 source=re.sub(r'<p class="lead">.*?</p>',lambda m:'<p class="lead">'+data['intro']+'</p>',source,count=1)
 sections=data['sections']+[('Câu hỏi thường gặp',faq(data['faq']))]
 body='';toc=''
 for i,section in enumerate(sections,1):
  title=section[0];text=''.join(section[1:])
  sid='muc-'+str(i);body+=f'<section><h2 id="{sid}">{title}</h2>{text}</section>'
  toc+=f'<li><a href="#{sid}">{title}</a></li>'
 # Preserve the second editorial image on the booking guide.
 if slug=='huong-dan-dat-tai-xe-nhu-y-driver':
  image=re.search(r'<img[^>]*src="assets/images/website/11_[^>]*>',source)
  if image:body+='<figure class="article-figure">'+image.group(0)+'<figcaption>Các bước liên hệ, xác nhận và hoàn tất chuyến đi tại Như Ý Driver.</figcaption></figure>'
 reading='<div class="reading">'+tags_html(data['tags'])+'<p class="editorial-meta">Biên soạn: Như Ý Driver · Cập nhật <time datetime="2026-10-27">27/10/2026</time></p><nav class="toc" aria-label="Mục lục"><strong>Trong bài viết</strong><ul>'+toc+'</ul></nav>'+body
 start=source.index('<div class="reading">');end=re.search(r'<section><h2>(?:Khám phá thêm|Đọc tiếp theo nhu cầu của bạn)</h2>',source[start:]).start()+start
 source=source[:start]+reading+source[end:]
 related='<section><h2>Đọc tiếp theo nhu cầu của bạn</h2><div class="related">'
 for target in data['related']:
  title=ARTICLES[target]['title'] if target in ARTICLES else LH.parse(str(ROOT/(target+'.html'))).xpath('//h1')[0].text_content()
  related+=a(target,title)
 related+='</div></section>'
 source=re.sub(r'<section><h2>(?:Khám phá thêm|Đọc tiếp theo nhu cầu của bạn)</h2>.*?</section>',lambda m:related,source,count=1,flags=re.S)
 image=doc.xpath('//meta[@property="og:image"]/@content')[0]
 schema={'@context':'https://schema.org','@type':'Article','headline':data['title'],'description':data['desc'],'image':[image],'inLanguage':'vi-VN','mainEntityOfPage':{'@type':'WebPage','@id':BASE+slug+'.html'},'url':BASE+slug+'.html','dateModified':'2026-10-27T23:00:00+07:00','author':{'@type':'Organization','name':'Như Ý Driver','url':BASE},'publisher':{'@type':'Organization','name':'Như Ý Driver','url':BASE,'logo':{'@type':'ImageObject','url':BASE+'assets/images/logo.png'}},'keywords':data['tags']}
 source=source.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script></head>',1)
 # Do not make up a publication date; the page shows its real editing date only.
 source=source.replace('2026-10-27T23:00:00+07:00','2026-10-27')
 file.write_text(source,encoding='utf-8')

# Give the service pages topic navigation too, without creating duplicate tag pages.
SERVICE_TAGS={
'bang-gia-lai-xe-ho-da-nang':['Bảng giá','Ô tô','Xe máy'],
'lai-xe-ho-sau-tiec-da-nang':['Sau tiệc','Lái xe hộ','Ban đêm'],
'lai-xe-ho-o-to-da-nang':['Ô tô','Lái xe hộ'],
'lai-xe-ho-xe-may-da-nang':['Xe máy','Lái xe hộ'],
'thue-tai-xe-theo-gio-da-nang':['Theo giờ','Ô tô'],
'thue-tai-xe-theo-ngay-da-nang':['Theo ngày','Ô tô'],
'thue-tai-xe-di-tinh-da-nang':['Đi tỉnh','Ô tô'],
'khu-vuc-phuc-vu':['Khu vực','Lái xe hộ']}
for slug,tags in SERVICE_TAGS.items():
 file=ROOT/(slug+'.html');s=file.read_text(encoding='utf-8')
 s=s.replace('<div class="reading">','<div class="reading">'+tags_html(tags),1)
 file.write_text(s,encoding='utf-8')

# Keep the card titles, excerpts, search data and image labels in sync with their pages.
file=ROOT/'tin-tuc.html';source=file.read_text(encoding='utf-8')
def card_update(match):
 card=match.group();slug=re.search(r'href="([a-z0-9-]+)\.html"',card).group(1)
 d=ARTICLES.get(slug)
 if not d:
  doc=LH.parse(str(ROOT/(slug+'.html')));title=doc.xpath('//h1')[0].text_content();intro=doc.xpath('//p[@class="lead"]')[0].text_content();tags=SERVICE_TAGS[slug]
 else:title=d['title'];intro=d['intro'];tags=d['tags']
 card=re.sub(r'data-search="[^"]*"',lambda m:'data-search="'+html.escape(title+' '+intro+' '+' '.join(tags),quote=True)+'" data-topics="'+html.escape('|'.join(tags),quote=True)+'"',card,count=1)
 card=re.sub(r'(<h3><a href="[^"]+">).*?(</a></h3>)',lambda m:m.group(1)+html.escape(title)+m.group(2),card,count=1)
 card=re.sub(r'<p>.*?</p>',lambda m:'<p>'+html.escape(intro)+'</p>',card,count=1)
 return card
source=re.sub(r'<article class="card"[^>]*>.*?</article>',card_update,source,flags=re.S)
source=source.replace('<section class="news-search">','<section class="news-search" id="noi-dung">',1)
tags=['Lái xe hộ','Bảng giá','Ô tô','Xe máy','Sau tiệc','Ban đêm','Theo giờ','Theo ngày','Đi tỉnh','Bàn giao xe','Đặt tài xế','Taxi','Xe thuê tự lái','Khu vực']
filters='<div class="topic-filters" role="group" aria-label="Lọc theo chủ đề"><button type="button" data-topic="" aria-pressed="true">Tất cả</button>'+''.join(f'<button type="button" data-topic="{t}" aria-pressed="false">#{t}</button>' for t in tags)+'</div>'
source=source.replace('<p id="search-status"',filters+'<p id="search-status"',1)
source=source.replace('Chọn nội dung để xem chi tiết.','Tìm câu trả lời cho chuyến đi của bạn, hoặc chọn một chủ đề bên dưới để xem bài liên quan.')
# Article schema is kept on detail pages; news remains a single indexable hub.
file.write_text(source,encoding='utf-8')

script=ROOT/'assets/js/content.js';s=script.read_text(encoding='utf-8')
tracking=s[s.index('document.querySelectorAll(\'a[href="tel:'):]
filter_script='''const input = document.querySelector('#article-search');
if (input) {
  const normalize = value => value.toLocaleLowerCase('vi').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/đ/g, 'd');
  const cards = [...document.querySelectorAll('[data-search]')];
  const buttons = [...document.querySelectorAll('[data-topic]')];
  const params = new URLSearchParams(window.location.search);
  const requestedTopic = params.get('chu-de') || '';
  let topic = buttons.some(button => button.dataset.topic === requestedTopic) ? requestedTopic : '';
  input.value = params.get('q') || '';
  const applyFilter = () => {
    const query = normalize(input.value.trim()); let count = 0;
    cards.forEach(card => {
      const topics = (card.dataset.topics || '').split('|');
      card.hidden = !(normalize(card.dataset.search).includes(query) && (!topic || topics.includes(topic)));
      if (!card.hidden) count++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.topic === topic)));
    document.querySelector('#search-status').textContent = count ? `${count} nội dung${topic ? ' về ' + topic : ''}` : 'Không tìm thấy nội dung. Hãy thử từ khóa khác hoặc chọn Tất cả.';
    ['dich-vu', 'bai-viet'].forEach(id => {
      const section = document.getElementById(id);
      if (section) section.hidden = ![...section.querySelectorAll('.card')].some(card => !card.hidden);
    });
  };
  const rememberFilters = () => {
    const url = new URL(window.location.href);
    if (topic) url.searchParams.set('chu-de', topic); else url.searchParams.delete('chu-de');
    if (input.value.trim()) url.searchParams.set('q', input.value.trim()); else url.searchParams.delete('q');
    window.history.replaceState(null, '', url);
  };
  input.addEventListener('input', () => { applyFilter(); rememberFilters(); });
  buttons.forEach(button => button.addEventListener('click', () => { topic = button.dataset.topic; applyFilter(); rememberFilters(); }));
  applyFilter();
}
'''
script.write_text(filter_script+tracking,encoding='utf-8')
css='''
.topic-tags,.topic-filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:24px 0}
.topic-tags a,.topic-filters button{font:inherit;font-size:14px;line-height:1.5;border:1px solid #d8dde3;border-radius:6px;padding:8px 12px;background:#f7f8fa;color:#84202c;text-decoration:none;cursor:pointer}
.topic-tags span{font-size:14px;color:#526173;margin-right:4px}
.topic-tags a:hover,.topic-filters button:hover{background:#f3e9e9;border-color:#a52936}
.topic-filters button[aria-pressed=true]{background:#9e1824;color:white;border-color:#9e1824}
.topic-filters button:focus-visible{outline:3px solid #bd8f2e;outline-offset:3px}
.editorial-meta{font-size:13px;color:#5a6877;margin:18px 0}.article-figure{margin:28px 0}.article-figure img{width:100%;max-width:650px;margin:auto}.article-figure figcaption{font-size:13px;color:#536171;text-align:center;margin-top:12px}
.reading blockquote{margin:22px 0;padding:20px 24px;background:#f6f3ee;border-left:4px solid #be943b}
[hidden]{display:none!important}
'''
file=ROOT/'assets/css/content.css';file.write_text(file.read_text(encoding='utf-8')+css,encoding='utf-8')
# These topic controls occur inside main on the news hub; scoped rules preserve its home shell.
file=ROOT/'assets/css/news-content.css'
scoped=css.replace('.topic-', '.news-content .topic-').replace('.editorial-meta','.news-content .editorial-meta').replace('.article-figure','.news-content .article-figure').replace('.reading blockquote','.news-content .reading blockquote').replace('[hidden]','.news-content [hidden]')
file.write_text(file.read_text(encoding='utf-8')+scoped,encoding='utf-8')

# lastmod reflects this editorial update on the 11 revised guide URLs only.
file=ROOT/'sitemap.xml';s=file.read_text(encoding='utf-8')
for slug in ARTICLES:
 loc='<loc>'+BASE+slug+'.html</loc>'
 s=s.replace(loc,loc+'<lastmod>2026-10-27</lastmod>')
file.write_text(s,encoding='utf-8')
print('Rewrote 11 guides; added Article data, topic links, hub filters and matching excerpts.')
