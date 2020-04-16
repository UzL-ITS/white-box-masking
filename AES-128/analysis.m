%% read the .txt data
rkey=hex2dec({'2b' '7e' '15' '16' '28' 'ae' 'd2' 'a6' 'ab' 'f7' '15'...
             '88' '09' 'cf' '4f' '3c'});
fid = fopen('trace.txt','r','n','ASCII');  % read traces
%fid2 = fopen('plaintext.txt','r','n','ASCII'); % read Plaintexes

fileID = fopen('plaintext.txt','r');
formatSpec = '%d';
sizeA = [16 Inf];
ptx = fscanf(fileID,formatSpec,sizeA)';


trace=[];
ntraces=500;

for i=1:ntraces
    trace(i,:) =  str2num(cell2mat(cellstr(fgetl(fid)')));

end


'Reading Complete'

%%
% Correlation Based DPA for each bit

[ntraces,~]=size(trace);
keybytes=zeros(1,16);
for bt=1:1
    
    ctx=zeros(ntraces,256);

    for i =0:255
       ctx(:,i+1)=  AES_Sbox(ptx(1:ntraces,bt),i);   
    end

    for j=1:8
        
        H=bitget(ctx,j);
        
        R=corr(H,trace);
        figure(bt),
        subplot(2,4,j)
        plot(R','Color',[0.7 0.7 0.7],'HandleVisibility','off')
        hold on
        %R=R(:,10:size(trace,2));
              
        [ind,~]=find(abs(R)==max(max(abs(R(:,1:size(trace,2))))));
        figure(bt),plot(R(ind,:)','LineWidth',1.2,'Color',[0.345 0.563 0.69])
        %figure(bt),plot(R(rkey(bt)+1,:)','LineWidth',1.2,'Color', [0.91 0.28 0.28])
        %title(sprintf('max Corr is: 0x%c%c wrt %d th bit',dec2hex(ind(1)-1),1))
        legend({'Best Key Cand','Correct Key'})
        set(gca,'FontSize',24)
        set(findall(gcf,'type','text'),'FontSize',24)


        %title('Classification Results','FontSize', 26)
        ylabel('Correlation','FontSize', 28)
        hold off
    end
end
%%

[ntraces,~]=size(trace);
keybytes=zeros(1,16);
for bt=1:1
    
    ctx=zeros(ntraces,256);

    for i =0:255
       ctx(:,i+1)=  AES_Sbox(ptx(1:ntraces,bt),i);   
    end

   
        
    H=bitget(ctx,8);

    R=corr(H,trace);
    figure(bt),
    plot(R','Color',[0.7 0.7 0.7],'HandleVisibility','off')
    hold on
    %R=R(:,10:size(trace,2));

    [ind,~]=find(abs(R)==max(max(abs(R(:,1:size(trace,2))))));
    figure(bt),plot(R(ind,:)','LineWidth',1.4,'Color',[0.345 0.563 0.69])
    %figure(bt),plot(R(rkey(bt)+1,:)','LineWidth',1.2,'Color', [0.91 0.28 0.28])
    %title(sprintf('max Corr is: 0x%c%c wrt %d th bit',dec2hex(ind(1)-1),1))
    legend({'Best Key Cand','Correct Key'},'Location','northwest')
    set(gca,'FontSize',24)
    set(findall(gcf,'type','text'),'FontSize',24)


    %title('Classification Results','FontSize', 26)
    ylabel('Correlation','FontSize', 28)
    xlabel('Circuit Node','FontSize', 28)
    hold off
    
end

%% FvR test

s1=[ ]; 
s0=[ ];
c1=1;
c0=1;
for i=1:ntraces
    if(ptx(i,1)==0 && ptx(i,2)==0 && ptx(i,3)==0 && ptx(i,4)==0 && ptx(i,5)==0 )
        s1(:,c1)=trace(i,1:size(trace,2));
        c1=c1+1;
    else
       s0(:,c0)=trace(i,1:size(trace,2));
       c0=c0+1;
    end
end

t_test=(mean(s1')-mean(s0'))./(sqrt(var(s1')/size(s1,2)+var(s0')/size(s0,2)));



plot(t_test','Color',[0.7 0.7 0.7],'HandleVisibility','off')
hold on
[ind,~]=find(abs(t_test)==max(max(abs(t_test(:,1:size(trace,2))))));
figure(1),plot(t_test(ind,:)','LineWidth',1.4,'Color',[0.345 0.563 0.69])
%figure(bt),plot(R(rkey(bt)+1,:)','LineWidth',1.2,'Color', [0.91 0.28 0.28])
%title(sprintf('max Corr is: 0x%c%c wrt %d th bit',dec2hex(ind(1)-1),1))
%legend({'Best Key Cand','Correct Key'},'Location','northwest')
set(gca,'FontSize',24)
set(findall(gcf,'type','text'),'FontSize',24)


%title('Classification Results','FontSize', 26)
ylabel('$t$-test value','FontSize', 28,'Interpreter','latex')
xlabel('Circuit Node','FontSize', 28,'Interpreter','latex')

hline1 = refline([0 4.5]);
hline1.Color = 'r';

hline2 = refline([0 -4.5]);
hline2.Color = 'r';

hold off
